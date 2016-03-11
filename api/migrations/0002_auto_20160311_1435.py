# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 14:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expertcomment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expert_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usercomment',
            name='moderated',
            field=models.BooleanField(default=False, verbose_name='Moderado'),
        ),
    ]