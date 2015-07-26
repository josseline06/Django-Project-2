# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.utils.storage


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150720_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(storage=app.utils.storage.MyFileSystemStorage(), null=True, upload_to=app.utils.storage.upload_file, blank=True),
        ),
    ]
