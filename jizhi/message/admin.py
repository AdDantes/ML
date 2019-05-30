from django.contrib import admin
from .models import *
# Register your models here.


#将需要后台管理的model注册到admin后台
class MessageContentsAdmin(admin.ModelAdmin):
    #定制哪些字段需要在后台显示
    list_display = ['mess_username','mess_contents','mess_time']
admin.site.register(MessageContents,MessageContentsAdmin)