from django_gravatar import helpers as gravatar
from app.models import User, Location, Profile
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import json

# Genera un nombre clave 
def create_key_name(string):
	result = string.lowercase()
	return result.replace(' ', '_')

# Envio de correo
def send_email(destination,subject,variables,template):
	template_name = get_template('email/'+ template +'.text')

	to, from_email = destination , 'OWL Express <mail@owlexpress.me>'
	content = template_name.render(variables)
	msg = EmailMessage(subject, content, from_email, [to])
	msg.send()

# Calcula el costo de un paquete 
def package_cost(rate, width, height, depth, weight, price):
	return (width*height*depth*weight)/rate.value + (rate.percent*price)/100

# ----- Caso modificaciones sobre el modelo User y Profile -----
# Crea una lugar: 
def create_location(address, postal_code, city, country):
	try:
		location = Location.objects.get(address=address, postal_code=postal_code, city=city, country=country)
		print location
	except Location.DoesNotExist:
		location = Location(address=address, postal_code=postal_code, city=city, country=country)
		location.save()
	return location

# Sube un avatar
def upload_avatar(instance, filename):
	os.rename(filename, gravatar.calculate_gravatar_hash(instance.email))
	return os.path.join("avatars", filename)

# Verifica si avatar es proveniente de gravatar
def gravatar_avatar(instance):
	return instance.social_avatar == gravatar.get_gravatar_url(email=instance.email, default='identicon')

def create_gravatar(email):
	return gravatar.get_gravatar_url(email=email, default='identicon')
	
# Guarda un avatar
class OverwriteStorage(FileSystemStorage):
	def get_available_name(self, name):
		if self.exists(name):
			os.remove(os.path.join(settings.MEDIA_ROOT, name))
		return name

# Crea el perfil basico de un usuario:
def create_user(form, avatar):
	if not form.is_valid():
		return json.dumps({'profile': None, 'message':' Form is not valid, try again.'})
	data = form.cleaned_data
	try:
		user = User.objects.get(email=data['email'])
	except User.DoesNotExist:
		if not avatar:
			avatar = create_gravatar(data['email'])
		#Creando usuario:
		user = User.objects.create_user(data['email'], data['email'], data['password'])
		user.first_name = data['name']
		user.last_name = data['last_name']
		user.save()
		location = create_location(data['address'], data['postal_code'], data['city'], data['country'])
		profile = Profile(user=user, location=location, phone=data['phone'], social_avatar=avatar)
		profile.save()
		print profile
		return json.dumps({'profile': serializers.serialize('json', [ profile, ]), 'message': 'OK.'})
	return json.dumps({'profile': None, 'message': 'This email already exists, try again.'})