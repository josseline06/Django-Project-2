from django_gravatar import helpers as gravatar
from app.models import User, Location, Profile
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core import serializers
import json

# Genera un nombre clave 
def create_key_name(string):
	result = string.lowercase()
	return result.replace(' ', '_')

# Envio de correo
def send_email(destination,subject,variables):
	template_name = get_template('email/welcome.text')

	to, from_email = destination , 'OWL Express <mail@owlexpress.me>'
	content = template_name.render(variables)
	msg = EmailMessage(subject, content, from_email, [to])
	msg.send()

	#send_mail('Prueba de correo #1', 'Esto es un correo desde mi servidor yupi', 'OWL Express <mail@owlexpress.me>', [destinations], fail_silently=False)

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
		print 'llegom a esta puta mierda'
		location = Location(address=address, postal_code=postal_code, city=city, country=country)
		location.save()
	return location

# Crea el perfil basico de un usuario:
def create_user(form, avatar):
	if not form.is_valid():
		return json.dumps({'profile': None, 'message':' Form is not valid'})
		
	try:
		user = User.objects.get(email=form.cleaned_data['email'])
	except User.DoesNotExist:
		if not avatar:
			avatar = gravatar.get_gravatar_url(email=form.cleaned_data['email'], default='identicon')
		#Creando usuario:
		user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['email'], form.cleaned_data['password'])
		user.first_name = form.cleaned_data['name']
		user.last_name = form.cleaned_data['last_name']
		user.save()
		location = create_location(form.cleaned_data['address'], form.cleaned_data['postal_code'], form.cleaned_data['city'], form.cleaned_data['country'])
		profile = Profile(user=user, location=location, phone=form.cleaned_data['phone'], social_avatar=avatar)
		profile.save()
		print profile
		return json.dumps({'profile': serializers.serialize('json', [ profile, ]), 'message': 'OK'})
	return json.dumps({'profile': None, 'message': 'This email already exists'})