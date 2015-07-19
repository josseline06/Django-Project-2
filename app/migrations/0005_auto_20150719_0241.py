# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_load_initial_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipment',
            name='location',
        ),
        migrations.AddField(
            model_name='shipment',
            name='destination',
            field=models.OneToOneField(related_name='shipment_destination_fk', to='app.Location'),
            preserve_default=False,
        ),
    ]
