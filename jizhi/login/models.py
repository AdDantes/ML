from django.db import models

# Create your models here.
class BaseModel(models.Model):
    # 逻辑删除字段
    isDelete = models.BooleanField(default=False)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)

    #元选项
    class Meta:
        #告诉Django这个类是一个抽象类，不需要为本类创建数据库表
        abstract = True

class Register(BaseModel):
    reg_userName = models.CharField(max_length=50)
    reg_passWord = models.CharField(max_length=20)
    def __str__(self):
        return '%s:%s'% (self.reg_userName,self.reg_passWord)
