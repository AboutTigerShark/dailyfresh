from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname =  models.CharField(max_length=20)  # 用户名
    upwd = models.CharField(max_length=40)  # 密码
    uemail = models.CharField(max_length=30)  # 邮箱
    ureceive = models.CharField(max_length=20, default='')  # 快递接收者
    uadress = models.CharField(max_length=120, default='')  # 送货地址
    uzipcode = models.CharField(max_length=6, default='')  # 邮编
    uphonenumber = models.CharField(max_length=11, default='')  # 电话号码
    class Meta:
        db_table = 'userinfo'
