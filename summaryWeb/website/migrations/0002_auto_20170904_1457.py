# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-09-04 14:57
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_saveToEdit',
            field=models.BooleanField(default=False, verbose_name='save'),
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='comment',
            name='createDate',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='comment',
            name='profile_image',
            field=models.CharField(default='static/img/geek.jpg', max_length=250),
        ),
        migrations.AddField(
            model_name='comment',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='username'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_image_url',
            field=models.CharField(default='static/img/geek.jpg', max_length=250),
        ),
        migrations.AlterField(
            model_name='article',
            name='pubmedID',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='belong_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.FileField(blank=True, null=True, upload_to='avatar', verbose_name='profile'),
        ),
    ]
