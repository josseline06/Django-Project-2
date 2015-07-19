from enum import Enum
from django_gravatar import helpers as gravatar
from app.models import User, Location, Profile

# Genera un nombre clave 
def create_key_name(string):
	result = string.lowercase()
	return result.replace(' ', '_')

# Calcula el costo de un paquete 
def package_cost(rate, width, height, depth, weight, price):
	return (width*height*depth*weight)/rate.value + (rate.percent*price)/100

# ----- Caso modificaciones sobre el modelo User y Profile -----
# Crea una lugar: 
def create_location(address, postal_code, city, country):
	try:
		location = Location.objects.get(address=address, postal_code=postal_code, city=city, country=country)
	except Location.DoesNotExist:
		location = Location(address=address, postal_code=postal_code, city=city, country=country)
		location.save()
	return location

# Crea el perfil basico de un usuario:
# Estados:
class states(Enum):
	ok = 1
	form_no_valid = 2
	email_exists = 3
	
state = states.ok

def create_user(form, avatar):
	if not form.is_valid():
		state = states.form_no_valid
		return None

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

		state = states.ok
		return profile

	state = states.email_exists
	return None