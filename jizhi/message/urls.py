
from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^index',index),
    url('^handle/$',message_handle),
    url('^show/$',message_show), #位置参数捕获
]
