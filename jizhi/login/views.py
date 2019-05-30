from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
# Create your views here.

def login(request):
    """
    显示登陆页面
    :param request:
    :return:
    """
    return render(request,'login/login.html')

def login_check(request):
    """
    登录验证
    :param request:
    :return:
    """
    #获取用户名、密码
    username = request.POST['username']
    password = request.POST.get('password')
    #根据用户名、密码查询数据库
    if username=='liangchen' and password == '123':
        #页面重定向
        #如果用户名密码正确，跳转到首页
        return HttpResponseRedirect('/message/index/')
    else:
        #用户名密码错误，跳转到登录页面，重新输入
        return HttpResponseRedirect('/login')

def register_show(request):
    """
    显示注册页面
    :param request:
    :return:
    """
    return render(request,'login/register.html')

def register_handle(request):
    """
    注册信息处理
    :param request:
    :return:
    """
    # 获取用户名、密码
    username = request.POST['username']
    password = request.POST.get('password')
    print(username,password)
    reg = Register()
    reg.reg_userName = username
    reg.reg_passWord = password
    reg.save()
    return HttpResponse("注册成功")