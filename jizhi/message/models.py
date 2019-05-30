from django.db import models



class BaseModel(models.Model):
    # 逻辑删除字段
    isDelete = models.BooleanField(default=False)
    # 创建时间
    mess_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)

    #元选项
    class Meta:
        #告诉Django这个类是一个抽象类，不需要为本类创建数据库表
        abstract = True
        #db_table改变默认的数据库表的名字
        db_table = 'message_contents'

# Create your models here.
class MessageContents(BaseModel):
    """
    留言内容表
    """
    mess_username = models.CharField(max_length=20)
    mess_contents = models.CharField(max_length=200)
    # #自定义管理器
    # my_objects = models.Manager()
