# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-09-07 08:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_article_pubmedidurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='pubmedIDurl',
        ),
    ]
