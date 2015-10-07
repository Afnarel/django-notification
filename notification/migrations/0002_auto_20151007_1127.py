# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticetype',
            name='description_de',
            field=models.CharField(null=True, max_length=100, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='noticetype',
            name='description_fr',
            field=models.CharField(null=True, max_length=100, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='noticetype',
            name='description_it',
            field=models.CharField(null=True, max_length=100, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='noticetype',
            name='display_de',
            field=models.CharField(null=True, max_length=50, verbose_name='display'),
        ),
        migrations.AddField(
            model_name='noticetype',
            name='display_fr',
            field=models.CharField(null=True, max_length=50, verbose_name='display'),
        ),
        migrations.AddField(
            model_name='noticetype',
            name='display_it',
            field=models.CharField(null=True, max_length=50, verbose_name='display'),
        ),
        migrations.AlterField(
            model_name='noticesetting',
            name='medium',
            field=models.CharField(verbose_name='medium', max_length=1, choices=[('0', 'email'), ('2', 'mobile'), ('1', 'site')]),
        ),
    ]
