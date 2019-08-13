from django.db import models


class CartInfo(models.Model):
    user = models.ForeignKey('user_manage.UserInfo')
    goods = models.ForeignKey('goods_manage.GoodsInfo')
    count = models.IntegerField()
