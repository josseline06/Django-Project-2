# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=254, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='employee_agency_fk', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=1000)),
                ('postal_code', models.CharField(max_length=15)),
                ('city', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.DecimalField(max_digits=8, decimal_places=2)),
                ('width', models.DecimalField(max_digits=8, decimal_places=2)),
                ('height', models.DecimalField(max_digits=8, decimal_places=2)),
                ('depth', models.DecimalField(max_digits=8, decimal_places=2)),
                ('price', models.DecimalField(max_digits=12, decimal_places=2)),
                ('cost', models.DecimalField(max_digits=12, decimal_places=2)),
                ('description', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('social_avatar', models.URLField()),
                ('avatar', models.ImageField(null=True, upload_to=b'avatars/', blank=True)),
                ('last_edit', models.DateTimeField(auto_now_add=True)),
                ('is_manager', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('key_name', models.CharField(unique=True, max_length=15)),
                ('value', models.DecimalField(max_digits=12, decimal_places=2)),
                ('percent', models.DecimalField(max_digits=5, decimal_places=2)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('agency', models.ForeignKey(related_name='agency_fk', to='app.Agency')),
                ('checker', models.ForeignKey(related_name='checker_fk', to=settings.AUTH_USER_MODEL)),
                ('location', models.OneToOneField(related_name='shipment_location_fk', to='app.Location')),
                ('rate', models.ForeignKey(related_name='rate_fk', to='app.Rate')),
                ('receiver', models.ForeignKey(related_name='receiver_fk', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='sender_fk', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'created', max_length=9, choices=[(b'created', b'Created'), (b'dispached', b'Dispatched'), (b'received', b'Received'), (b'committed', b'Commited')])),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('profile', models.OneToOneField(related_name='employee_profile_fk', primary_key=True, serialize=False, to='app.Profile')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='rate',
            unique_together=set([('value', 'percent')]),
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.OneToOneField(related_name='user_location_fk', to='app.Location'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(related_name='profile_fk', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='package',
            name='shipment',
            field=models.ForeignKey(related_name='shipment_fk', to='app.Shipment'),
        ),
        migrations.AddField(
            model_name='agency',
            name='location',
            field=models.OneToOneField(related_name='agency_location_fk', to='app.Location'),
        ),
        migrations.AddField(
            model_name='agency',
            name='manager',
            field=models.OneToOneField(related_name='manager_fk', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='agency',
            field=models.ForeignKey(related_name='employee_agency_fk', to='app.Agency'),
        ),
    ]
