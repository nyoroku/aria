# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2021-11-12 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0008_product_pick'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='color',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
