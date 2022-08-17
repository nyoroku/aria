# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-17 18:05
from __future__ import unicode_literals

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_display'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplayAdvert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('body', models.TextField()),
                ('location', models.CharField(blank=True, max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('photo', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='latest')),
            ],
        ),
        migrations.DeleteModel(
            name='Display',
        ),
        migrations.DeleteModel(
            name='Testimonial',
        ),
    ]