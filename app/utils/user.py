from enum import Enum
from django_gravatar import helpers as gravatar
from app.models import *

class states(Enum):
	ok = 1
	form_no_valid = 2
	email_exists = 3
	
state = states.ok

def create_user(form, avatar):
	if not form.is_valid():
		state = states.form_no_valid
		return None

	user = User.objects.filter(email=form.cleaned_data['email'])

	if user.count() > 0:
		state = states.email_exists
		return None
	
	if not avatar:
		avatar = gravatar.get_gravatar_url(email=form.cleaned_data['email'], default='identicon')
				
	#Creando usuario:
	user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['email'], form.cleaned_data['password'])
	user.first_name = form.cleaned_data['name']
	user.last_name = form.cleaned_data['last_name']
	user.save()
	location = Location(address=form.cleaned_data['address'], postal_code=form.cleaned_data['postal_code'], city=form.cleaned_data['city'], country=form.cleaned_data['country'])
	location.save()
	profile = Profile(user=user, location=location, phone=form.cleaned_data['phone'], social_avatar=avatar)
	profile.save()

	state = states.ok
	return profile