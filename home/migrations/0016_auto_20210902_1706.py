# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-09-02 14:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20210831_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='displayadvert',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 2, 14, 6, 1, 343000, tzinfo=utc)),
        ),
    ]
