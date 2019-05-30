from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
# Create your views here.


def index(request):
    """
    显示留言视图
    :param request:
    :return:
    """
    #使用render函数渲染模板
    #渲染模板指的是：用数据去填充HTML页面中的某些位置
    response = render(request,'message/index.html')
    return response
def message_handle(request):
    """
    处理留言
    :param request:
    :return:
    """
    #获得表单数据
    username = request.POST['username']
    contents = request.POST['contents']
    #表单数据插入数据库中
    mc = MessageContents()
    mc.mess_username = username
    mc.mess_contents = contents
    mc.save()
    return HttpResponseRedirect('/message/show')

def message_show(request):
    """
    显示用户留言
    :param requset:
    :return:
    """

    messages = MessageContents.objects.all()
    response = render(request,'message/show.html',{'messages':messages})
    return response