# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-01 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='sightingfaq',
            name='quickBody',
            field=models.TextField(default=False, max_length=128, verbose_name='Breve explicación'),
        ),
        migrations.AlterField(
            model_name='sightingfaq',
            name='body',
            field=models.TextField(verbose_name='Explicación más detallada'),
        ),
    ]
