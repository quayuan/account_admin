from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        """
        展示
        :param request:
        :return:
        """
        return render(request, 'index.html')

    # def post(self, request):
    #     """
    #     跳转
    #     :param request:
    #     :return:
    #     """
    #     response = redirect('/user/register')
    #     return response


