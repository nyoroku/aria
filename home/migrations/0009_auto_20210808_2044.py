# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-08-08 17:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_displayadvert_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='displayadvert',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 8, 17, 44, 19, 498000, tzinfo=utc)),
        ),
    ]
