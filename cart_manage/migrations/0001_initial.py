# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0002_auto_20190731_0008'),
        ('goods_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='goods_manage.GoodsInfo')),
                ('user', models.ForeignKey(to='user_manage.UserInfo')),
            ],
        ),
    ]
