from django import forms
from phonenumber_field import formfields as phonefield
from .models import *

#Registro
class SignUpForm(forms.Form):
	name = forms.CharField(min_length=3, max_length=30)
	last_name = forms.CharField(min_length=2, max_length=30)
	email = forms.EmailField()
	password = forms.CharField(min_length=5, max_length=15)
	country = forms.CharField(min_length=3, max_length=30)
	city = forms.CharField(min_length=3, max_length=30)
	postal_code = forms.CharField(min_length=3, max_length=15)
	address = forms.CharField(min_length=5, max_length=1000)
	phone = phonefield.PhoneNumberField()

# Para empleado:
class EmployeeForm(SignUpForm):
	agency = forms.ChoiceField(choices=Agency.objects.filter(is_active=True))

# Para administrador:
class AdminForm(SignUpForm):
	is_manager = forms.BooleanField()

# Perfil
class ProfileForm(forms.Form):
	avatar = forms.ImageField(required=False)
	name = forms.CharField(min_length=3, max_length=30)
	last_name = forms.CharField(min_length=2, max_length=30)
	email = forms.EmailField()
	country = forms.CharField(min_length=3, max_length=30)
	city = forms.CharField(min_length=3, max_length=30)
	postal_code = forms.CharField(min_length=3, max_length=15)
	address = forms.CharField(min_length=5, max_length=1000)
	phone = phonefield.PhoneNumberField()

# Calculadora de envio
class CalculatorForm(forms.Form):
	weight = forms.DecimalField(min_value=0.01, max_digits=8, decimal_places=2)
	width = forms.DecimalField(min_value=0.01, max_digits=8, decimal_places=2)
	height = forms.DecimalField(min_value=0.01, max_digits=8, decimal_places=2)
	depth = forms.DecimalField(min_value=0.01, max_digits=8, decimal_places=2)
	price = forms.DecimalField(min_value=0.01, max_digits=12, decimal_places=2)

# Agencia
class AgencyForm(forms.Form):
	address = forms.CharField(min_length=5, max_length=1000)
	city = forms.CharField(max_length=30)
	country = forms.CharField(max_length=30)
	phone = phonefield.PhoneNumberField()
	manager = forms.ChoiceField(choices=User.objects.filter(is_active=True, groups__name='managers'))

# Tarifa
class RateForm(forms.Form):
	name = forms.CharField(min_length=5, max_length=30)
	value = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01) #Constante 
	percent = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0.01) #K%
	description = forms.CharField(max_length=1000)

# Paquete
class PackageForm(forms.Form):
	weight = forms.DecimalField(min_value=0.01, max_digits=8, decimal_places=2)
	width = forms.DecimalField(min_value=0.01, max_digits=8, decimal_places=2)
	height = forms.DecimalField(min_value=0.01, max_digits=8, decimal_places=2)
	depth = forms.DecimalField(min_value=0.01, max_digits=8, decimal_places=2)
	price = forms.DecimalField(min_value=0.01, max_digits=12, decimal_places=2)
	cost = forms.DecimalField(min_value=0.01, max_digits=12, decimal_places=2)
	description = forms.CharField(required=False, max_length=1000)

# Envio
class ShipmentForm(forms.Form):
	sender = forms.ChoiceField(choices=User.objects.filter(is_active=True, groups__name='clients'))
	receiver = forms.ChoiceField(choices=User.objects.filter(is_active=True, groups__name='clients'))
	rate = forms.ChoiceField(choices=Rate.objects.filter(is_active=True))
	address = forms.CharField(min_length=5, max_length=1000)
	country = forms.CharField(min_length=3, max_length=30)
	city = forms.CharField(min_length=3, max_length=30)
	postal_code = forms.CharField(min_length=3, max_length=15)
	description = forms.CharField(max_length=1000, required=False)

# Status de envio
class StatusForm(forms.ModelForm):
	class Meta:
		model = Status
		fields = ['status']

# Comentarios
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment']