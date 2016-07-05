# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 06:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupon_models', '0004_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='avatar',
            field=models.ImageField(default='user/images/avatar-placeholder.png', upload_to='sale/avatar', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='finish_date',
            field=models.DateTimeField(verbose_name='\u0425\u044f\u043c\u0434\u0440\u0430\u043b \u0434\u0443\u0443\u0441\u0430\u0445 \u04e9\u0434\u04e9\u0440'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='start_date',
            field=models.DateTimeField(verbose_name='\u0425\u044f\u043c\u0434\u0440\u0430\u043b \u044d\u0445\u044d\u043b\u0441\u044d\u043d \u04e9\u0434\u04e9\u0440'),
        ),
    ]