from django.shortcuts import render
from django.views import View
from django import http
import re
import logging


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
        # 输出日志
        logger.info('user_name')
        logger.info('pwd')
        logger.info('cpwd')

        if not all([user_name, pwd, cpwd, server_type]):
            return http.HttpResponseBadRequest('请填写完整信息')
        # 用户名格式
        if not re.match('^[a-zA-Z0-9_-]{5,20}$', user_name):
            return http.HttpResponseBadRequest('请输入5-20个字符的用户名')
        # 用户名是否存在

        # 2.4密码格式
        if not re.match('^[0-9A-Za-z]{8,20}$', pwd):
            return http.HttpResponseBadRequest('请输入8-20位的密码')
        # 2.5两个密码是否一致
        if pwd != cpwd:
            return http.HttpResponseBadRequest('两个密码不一致')

        response = {
            'user_name': user_name,
            'password': pwd,
            'check_password': cpwd,
            'server_type': server_type
        }

        return http.JsonResponse(response)
