# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command

fixtures = ['groups.json', 'admins.json']

def load_fixture(apps, schema_editor):
	for fixture in fixtures:
		call_command('loaddata', fixture, app_label='app') 

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150718_2224'),
    ]

    operations = [
    	migrations.RunPython(load_fixture),
    ]