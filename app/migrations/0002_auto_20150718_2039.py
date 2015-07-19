# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agency',
            name='id',
        ),
        migrations.RemoveField(
            model_name='rate',
            name='id',
        ),
        migrations.AddField(
            model_name='agency',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 19, 1, 8, 41, 477608, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agency',
            name='key_name',
            field=models.CharField(default='key_name_agency', max_length=60, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agency',
            name='name',
            field=models.CharField(default='Agency Name', unique=True, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rate',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 19, 1, 9, 18, 509666, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rate',
            name='key_name',
            field=models.CharField(max_length=60, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='name',
            field=models.CharField(unique=True, max_length=60),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('address', 'postal_code', 'city', 'country')]),
        ),
    ]
