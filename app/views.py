from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View, TemplateView
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group
from django.shortcuts import render
from .utils import * as utils
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

# Registro de clientes
class SignUp(View):
	def post(self, request):
		sign_up	= SignUpForm(request.POST, request.FILES)
		
		profile = utils.create_user(sign_up,request.POST['avatar'])
		if not profile:
			if utils.state == utils.states.form_no_valid:
				return JsonResponse({"response": "Error"})
			if utils.state == utils.states.email_exists:	
				return JsonResponse({"response": "This email already exists"})
		
		# Asignando grupo:
		group = Group.objects.get(name='clients')
		profile.user.groups.add(group)

		return JsonResponse({"response": "Yeah"})

# Registro de empleados
@login_required
@permission_required('app.add_employeeprofile')
class NewEmployee(View):
	def post(self, request):
		new_employee = EmployeeForm(request.POST, request.FILES)
		
		profile = utils.create_user(new_employee,request.POST['avatar'])
		if not profile:
			if utils.state == utils.states.form_no_valid:
				return JsonResponse({"response": "Error"})
			if utils.state == utils.states.email_exists:	
				return JsonResponse({"response": "This email already exists"})
		# Agregando agencia:
		employee = EmployeeProfile(profile=profile, new_employee.cleaned_data['agency'])
		employee.save()
		# Asignando grupo:
		group = Group.objects.get(name='employees')
		profile.user.groups.add(group)

		return JsonResponse({"response": "Yeah"})

# Registro de administradores
@login_required
@permission_required('app.add_agency')
class NewAdmin(View):
	def post(self, request):
		new_admin = AdminForm(request.POST, request.FILES)
		
		profile = utils.create_user(new_admin,request.POST['avatar'])
		if not profile:
			if utils.state == utils.states.form_no_valid:
				return JsonResponse({"response": "Error"})
			if utils.state == utils.states.email_exists:	
				return JsonResponse({"response": "This email already exists"})
		# Verificando si es gerente de agencia:
		if new_admin.cleaned_data['is_manager']:
			profile.is_manager = True
			profile.save()
			group_name = 'managers'
		else:
			group_name = 'administrators'

		# Asignando grupo:
		group = Group.objects.get(name=group_name)
		profile.user.groups.add(group)

		return JsonResponse({"response": "Yeah"})

# Registro de agencias
@login_required
@permission_required('app.add_agency')
class NewAgency(View):
	def post(self, request):
		new_agency = AgencyForm(request.POST, request.FILES)

		if not new_agency.is_valid():
			return JsonResponse({"response": "Error"})

		# Agregando nueva agencia:
		key_name = utils.create_key_name(new_agency.cleaned_data['name'])
		try:
			agency = Agency.objects.get(key_name=key_name)
			return JsonResponse({"response": "An agency already exists in that name"})
		except Agency.DoesNotExist:
			location = utils.create_location(new_agency.cleaned_data['address'], new_agency.cleaned_data['postal_code'], new_agency.cleaned_data['city'], new_agency.cleaned_data['country'])
			try:
				agency = Agency.objects.get(location=location)
				return JsonResponse({"response": "An agency already exists in that address"})
			except Agency.DoesNotExist:
				agency = Agency(key_name=key_name, name=new_agency.cleaned_data['name'], manager=new_agency.cleaned_data['manager'], location=location, phone=new_agency.cleaned_data['phone'])
				agency.save()
				return JsonResponse({"response": "Yeah"})

# Registro de tarifas
@login_required
@permission_required('app.add_rate')
class NewRate(View):
	def post(self, request):
		new_rate = RateForm(request.POST, request.FILES)

		if not new_rate.is_valid():
			return JsonResponse({"response": "Error"})

		# Agregando nueva agencia:
		key_name = utils.create_key_name(new_rate.cleaned_data['name'])
		try:
			rate = Rate.objects.get(key_name=key_name)
			return JsonResponse({"response": "An rate already exists with this name"})
		except Rate.DoesNotExist:
			try:
				rate = Rate.objects.get(value=new_rate.cleaned_data['value'], percent=new_rate.cleaned_data['percent'])
				return JsonResponse({"response": "An rate already exists with those values"})
			except Agency.DoesNotExist:
				rate = Rate(key_name=key_name, name=new_rate.cleaned_data['name'], value=new_rate.cleaned_data['value'], percent=new_rate.cleaned_data['percent'], description=new_rate.cleaned_data['description'])
				rate.save()
				return JsonResponse({"response": "Yeah"})

# Registro de envio:
