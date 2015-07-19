from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field import modelfields as phonemodel

class User(AbstractUser):
	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

# Modificando campos por default
User._meta.get_field('username').max_length = 254

class Location(models.Model):
	address = models.CharField(max_length=1000)
	postal_code = models.CharField(max_length=15)
	city = models.CharField(max_length=30)
	country = models.CharField(max_length=30)

	class Meta:
		unique_together = ('address','postal_code', 'city', 'country')

class Agency(models.Model):
	key_name = models.CharField(max_length=60, primary_key=True)
	name = models.CharField(max_length=60, unique=True)
	manager = models.OneToOneField(User, related_name='manager_fk', limit_choices_to=models.Q(groups__name = 'managers'))
	location = models.OneToOneField(Location, related_name='agency_location_fk')
	phone = phonemodel.PhoneNumberField()
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile_fk')
	location = models.OneToOneField(Location, related_name='user_location_fk')
	phone = phonemodel.PhoneNumberField()
	social_avatar = models.URLField()
	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
	last_edit = models.DateTimeField(auto_now_add=True)
	#Aplica solo para administradores:
	is_manager = models.BooleanField(default=False)
	
class EmployeeProfile(models.Model):	
	profile = models.OneToOneField(Profile, related_name='employee_profile_fk', primary_key=True)
	agency = models.ForeignKey(Agency, related_name='employee_agency_fk')

class Rate(models.Model):
	key_name = models.CharField(max_length=60, primary_key=True)
	name = models.CharField(max_length=60, unique=True)
	value = models.DecimalField(max_digits=12, decimal_places=2) #Constante 
	percent = models.DecimalField(max_digits=5, decimal_places=2) #K%
	date = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	description = models.CharField(max_length=1000)
	date_joined = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('value','percent')

class Shipment(models.Model):
	rate = models.ForeignKey(Rate, related_name='rate_fk') 
	sender = models.ForeignKey(User, related_name='sender_fk', limit_choices_to=models.Q(groups__name = 'clients'))
	receiver = models.ForeignKey(User, related_name='receiver_fk', limit_choices_to=models.Q(groups__name = 'clients'))
	checker = models.ForeignKey(User, related_name='checker_fk', limit_choices_to=models.Q(groups__name = 'employees'))
	agency = models.ForeignKey(Agency, related_name='agency_fk')
	location = models.OneToOneField(Location, related_name='shipment_location_fk')
	description = models.CharField(max_length=1000, null=True)

class Package(models.Model):
	shipment = models.ForeignKey(Shipment, related_name='shipment_fk')
	weight = models.DecimalField(max_digits=8, decimal_places=2)
	width = models.DecimalField(max_digits=8, decimal_places=2)
	height = models.DecimalField(max_digits=8, decimal_places=2)
	depth = models.DecimalField(max_digits=8, decimal_places=2)
	price = models.DecimalField(max_digits=12, decimal_places=2)
	cost = models.DecimalField(max_digits=12, decimal_places=2) 
	description = models.CharField(max_length=1000, null=True)

class Status(models.Model):
	STATUS = (
		('created', 'Created'),
		('dispached', 'Dispatched'),
		('received', 'Received'),
		('committed', 'Commited')
	)
	status = models.CharField(max_length=9, choices=STATUS, default='created')
	date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
	user = models.ForeignKey(User, related_name='employee_agency_fk', limit_choices_to=models.Q(groups__name = 'clients'))
	comment = models.CharField(max_length=1000)
	date = models.DateTimeField(auto_now_add=True)