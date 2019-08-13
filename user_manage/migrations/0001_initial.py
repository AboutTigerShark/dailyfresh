# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('uemail', models.CharField(max_length=30)),
                ('ureceive', models.CharField(max_length=20)),
                ('uadress', models.CharField(max_length=120)),
                ('uzipcode', models.CharField(max_length=6)),
                ('uphonenumber', models.CharField(max_length=11)),
            ],
            options={
                'db_table': 'userinfo',
            },
        ),
    ]
