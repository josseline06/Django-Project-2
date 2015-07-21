# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilelocation',
            name='location',
        ),
        migrations.RemoveField(
            model_name='profilelocation',
            name='location_ptr',
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.ForeignKey(related_name='profile_location_fk', default=1, to='app.Location'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ProfileLocation',
        ),
    ]
