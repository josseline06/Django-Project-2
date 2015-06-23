from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User)
	address = models.TextField()
	city = models.CharField(max_length=30)
	country = models.CharField(max_length=30)
	#Falta teléfono

# Agencia OWL Express
class Agency(models.Model):
	address = models.TextField()
	city = models.CharField(max_length=30)
	country = models.CharField(max_length=30)
	#Falta teléfono
	manager = models.OneToOneField(User) #gerente de la agencia

class Shipment(models.Model):
	cost = models.DecimalField(max_digits=12, decimal_places=2)
	description = models.TextField()
	sender = models.ForeignKey(User)
	receiver = models.ForeignKey(User)
	checker = models.ForeignKey(User)
	agency = models.ForeignKey(Agency)

class Package(models.Model):
	description = models.TextField()
	shipment = models.ForeignKey(Shipment)

class Status(models.Model):
	shipment = models.ForeignKey(Shipment)


