# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uadress',
            field=models.CharField(max_length=120, default=''),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uphonenumber',
            field=models.CharField(max_length=11, default=''),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='ureceive',
            field=models.CharField(max_length=20, default=''),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uzipcode',
            field=models.CharField(max_length=6, default=''),
        ),
    ]
