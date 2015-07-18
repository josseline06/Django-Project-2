from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View, TemplateView
from django_gravatar import helpers as gravatar
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group
from django.shortcuts import render
from .models import *
from .forms import *

# Pagina principal
class Index(View):
	template_name = 'index.html'
	form = EmployeeForm()

	def get(self, request):
		return render(request, self.template_name, {"form": self.form})

# Calculadora de precios
class Calculator(View):
	def post(self, request, rate):
		try:
			selected_rate = Rate.objects.get(key_name=rate)
		except Rate.DoesNotExist:
			selected_rate = None

		if selected_rate is None:
			#redireccionar a 404 template
			return JsonResponse({"response": "404 error"})
		
		calculator = CalculatorForm(request.POST, request.FILES)
		if not calculator.is_valid():
			return JsonResponse({"response": "error in data"})
		values = calculator.cleaned_data
		total = (values['width']*values['height']*values['depth']*values['weight'])/selected_rate.value + (selected_rate.selected_rate.percent*values['price'])/100
		return JsonResponse({"response": total})

# Registro de clientes,empleados y administradores
class SignUp(View):
	def post(self, request):
		if request.POST.get('agency'):
			sign_up	= EmployeeForm(request.POST, request.FILES)
			group_name = 'employees'
		elif request.POST.get('is_manager'):
			sign_up	= AdminForm(request.POST, request.FILES)
			if request.POST['is_manager']:
				group_name = 'managers'
			else:
				group_name = 'administrators'
		else:
			sign_up	= SignUpForm(request.POST, request.FILES)
			group_name = 'clients'

		if not sign_up.is_valid():
			return JsonResponse({"response": "Error"})
		
		if not request.POST['avatar']:
			url_avatar = gravatar.get_gravatar_url(email=request.POST['email'], default='identicon')
		else:
			url_avatar = request.POST['avatar']
			
		user = User.objects.filter(email=sign_up.cleaned_data['email'])

		if user.count() > 0:
			return JsonResponse({"response": "This email already exists"})

		#Creando usuario:
		user = User.objects.create_user(sign_up.cleaned_data['email'], sign_up.cleaned_data['email'], sign_up.cleaned_data['password'])
		user.first_name = sign_up.cleaned_data['name']
		user.last_name = sign_up.cleaned_data['last_name']
		user.save()
		location = Location(address=sign_up.cleaned_data['address'], postal_code=sign_up.cleaned_data['postal_code'], city=sign_up.cleaned_data['city'], country=sign_up.cleaned_data['country'])
		location.save()
		profile = Profile(user=user, location=location, phone=sign_up.cleaned_data['phone'], social_avatar=url_avatar)
		profile.save()
		if group_name == 'employees'
			employee = EmployeeProfile(profile=profile, agency=sign_up.cleaned_data['agency'])
			employee.save()

		group = Group.objects.get(name=group_name)
		user.groups.add(group)
		return JsonResponse({"response": "Yeah"})

