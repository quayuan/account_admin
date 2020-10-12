from django.shortcuts import render, redirect
from django.views import View
from django import http
import re
import time
import logging

from apscheduler.scheduler import Scheduler

from users.models import User
from .constant import file_path


def check_user_validity():
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    active_user_list = User.objects.filter(is_active=True)
    time_str = '# ' + str(now_time) + '\n'
    show_content = ''
    show_content += time_str
    for active_user in active_user_list:
        if active_user.is_superuser is True:
            continue
        else:
            name = active_user.username
            server_type = active_user.server_type
            pwd = active_user.password
            content = f'{name} {server_type} {pwd} *\n'
            show_content += content

    with open(file_path, 'w') as f:
        f.write(str(show_content))


sched = Scheduler()


@sched.interval_schedule(seconds=10)
def schedule_task():
    # logger = logging.getLogger('django')
    try:
        # logger.info('Timed task: Write user to file --- begin')
        check_user_validity()
        # logger.info('Timed task: Write user to file --- end')
    except Exception as e:
        raise 'Timed task error : ' + repr(e)


sched.start()


class RegisterView(View):
    """
    用户注册
    """

    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')

    def post(self, request):
        """
        创建用户对象，保存到表中
        """
        # 1.接收
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        server_type = request.POST.get('server_type')

        # 创建日志记录器
        logger = logging.getLogger('django')
        logger.info(f'user_name : {user_name}')
        logger.info(f'pwd : {pwd}')
        logger.info(f'cpwd : {cpwd}')
        logger.info(f'server_type : {server_type}')

        if not all([user_name, pwd, cpwd, server_type]):
            return http.HttpResponseBadRequest('请填写完整信息')
        # 用户名格式
        if not re.match('^[a-zA-Z0-9_-]{5,20}$', user_name):
            return http.HttpResponseBadRequest('请输入5-20个字符的用户名')
        # 用户名是否存在
        if User.objects.filter(username=user_name).count() > 0:
            return http.HttpResponseBadRequest('用户名已存在')
        # 2.4密码格式
        if not re.match('^[0-9A-Za-z_@.!]{8,20}$', pwd):
            return http.HttpResponseBadRequest("密码格式输入有误，请输入8-20位的密码(a~z, A~Z , 0~9 , '@' , '_' , '.', '!')")
        # 2.5两个密码是否一致
        if pwd != cpwd:
            return http.HttpResponseBadRequest('两次密码输入不一致')
        try:
            User.objects.create(username=user_name, password=pwd, server_type=server_type, is_active=False)

            response = {
                'user_name': user_name,
                'password': pwd,
                'check_password': cpwd,
                'server_type': server_type
            }
        except Exception as e:
            logger.error('Data write error : ', repr(e))
            error_response = {
                'status_code': 500,
                'error_info': '数据写入错误'
            }
            return http.JsonResponse(error_response)

        return http.JsonResponse(response)
