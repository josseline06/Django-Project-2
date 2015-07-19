# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150718_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='description',
            field=models.CharField(default='basic description', max_length=1000),
            preserve_default=False,
        ),
    ]
