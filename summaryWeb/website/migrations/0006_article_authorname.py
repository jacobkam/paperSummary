# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-09-05 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20170905_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='authorName',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='nickName'),
        ),
    ]
