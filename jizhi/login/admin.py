from django.contrib import admin
from .models import *
# Register your models here.


#将需要后台管理的model注册到admin后台
class RegisterUserAdmin(admin.ModelAdmin):
    #定制哪些字段需要在后台显示
    list_display = ['reg_userName','reg_passWord']
admin.site.register(Register,RegisterUserAdmin)
# Register your models here.
