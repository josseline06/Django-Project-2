from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View, TemplateView
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group
from django.shortcuts import render
from .models import *
from .forms import *
import .utils # helpers personalizados

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
			# Redireccionar a vista de 404
			return JsonResponse({"response": "404 error"})
		
		calculator = CalculatorForm(request.POST, request.FILES)
		if not calculator.is_valid():
			return JsonResponse({"response": "error in data"})
		data = calculator.cleaned_data
		total = utils.package_cost(selected_rate, data['width'], data['height'], data['depth'], data['weight'], data['price'])
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
class Employee(View):
	@permission_required('app.add_employeeprofile')
	def post(self, request):
		new_employee = EmployeeForm(request.POST, request.FILES)
		
		profile = utils.create_user(new_employee,request.POST['avatar'])
		if not profile:
			if utils.state == utils.states.form_no_valid:
				return JsonResponse({"response": "Error"})
			if utils.state == utils.states.email_exists:	
				return JsonResponse({"response": "This email already exists"})
		# Agregando agencia:
		employee = EmployeeProfile(profile=profile, agency=new_employee.cleaned_data['agency'])
		employee.save()
		# Asignando grupo:
		group = Group.objects.get(name='employees')
		profile.user.groups.add(group)

		return JsonResponse({"response": "Yeah"})

# Registro de administradores
@login_required
class Admin(View):
	@permission_required('app.add_agency')
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
class Agency(View):
	@permission_required('app.add_agency')
	def post(self, request):
		new_agency = AgencyForm(request.POST, request.FILES)

		if not new_agency.is_valid():
			return JsonResponse({"response": "Error"})

		# Agregando nueva agencia:
		data = new_agency.cleaned_data
		key_name = utils.create_key_name(data['name'])
		try:
			agency = Agency.objects.get(key_name=key_name)
		except Agency.DoesNotExist:
			location = utils.create_location(data['address'], data['postal_code'], data['city'], data['country'])
			try:
				agency = Agency.objects.get(location=location)
			except Agency.DoesNotExist:
				agency = Agency(key_name=key_name, name=data['name'], manager=data['manager'], location=location, phone=data['phone'])
				agency.save()
				return JsonResponse({"response": "Yeah"})
			return JsonResponse({"response": "An agency already exists in that address"})
		return JsonResponse({"response": "An agency already exists in that name"})


# Registro de tarifas
@login_required
class Rate(View):
	@permission_required('app.add_rate')
	def post(self, request):
		new_rate = RateForm(request.POST, request.FILES)

		if not new_rate.is_valid():
			return JsonResponse({"response": "Error"})

		# Agregando nueva tarifa:
		data = new_rate.cleaned_data
		key_name = general_utils.create_key_name(data['name'])
		try:
			rate = Rate.objects.get(key_name=key_name)
		except Rate.DoesNotExist:
			try:
				rate = Rate.objects.get(value=data['value'], percent=data['percent'])
			except Agency.DoesNotExist:
				rate = Rate(key_name=key_name, name=data['name'], value=data['value'], percent=data['percent'], description=data['description'])
				rate.save()
				return JsonResponse({"response": "Yeah"})
			return JsonResponse({"response": "An rate already exists with those values"})
		return JsonResponse({"response": "An rate already exists with this name"})

# Registro de envio:
@login_required
class Shipment(View):
	@permission_required('app.add_shipment')
	def post(self, request):
		new_shipment = ShipmentForm(request.POST, request.FILES)

		if not new_shipment.is_valid():
			return JsonResponse({"response": "Error"})

		data = new_shipment.cleaned_data
		destination = utils.create_location(data['address'], data['postal_code'], data['city'], data['country'])
		try:
			profile = Profile.objects.get(user=request.user)
			user = EmployeeProfile.objects.get(profile=profile)
		except (Profile.DoesNotExist, EmployeeProfile.DoesNotExist) as e:
			return JsonResponse({"response": "Error"})
		shipment = Shipment(rate=selected_rate, sender=data['sender'], receiver=data['receiver'], checker=request.user, agency=user.agency, destination=destination, description=data['description'])
		shipment.save()
		# Estatus creado:
		status = Status(shipment=shipment) 
		status.save()

		return JsonResponse({"response": "Yeah"})

# Registro de paquetes asociados a un envio:
@login_required
class Package(View):
	@permission_required('app.add_shipment')
	def post(self, request):
		new_package = PackageForm(request.POST, request.FILES)

		if not new_package.is_valid():
			return JsonResponse({"response": "Error"})

		data = new_package.cleaned_data
		cost = utils.package_cost(data['shipment'].rate, data['width'], data['height'], data['depth'], data['weight'], data['price'])
		package = Package(shipment=data['shipment'], weight=data['weight'], width=data['width'], height=data['height'], depth=data['depth'], price=data['price'], cost=cost, description=data['description'])
		package.save()

		return JsonResponse({"response": cost})

# Crear un comentario
@login_required
class Comment(View):
	@permission_required('app.add_comment')
	def post(self, request):
		new_comment = CommentForm(request.POST, request.FILES)

		if not new_comment.is_valid():
			return JsonResponse({"response": "Error"})

		data = new_package.cleaned_data
		comment = Comment(user=request.user, comment=data['comment'])
		comment.save()
