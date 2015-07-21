from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.contrib.auth.decorators import permission_required, login_required
from django.core import serializers
from django.contrib.auth.models import Group
from django.shortcuts import render
from .models import *
from .forms import *
from .utils import *
import json


# Pagina principal
class Index(View):
	template_name = 'index.html'
	def get(self, request):
		active_rates = Rate.objects.filter(is_active=True) #Retornando todos los planes de tarifas activos
		
		if active_rates.count() > 0:
			active_rates.description = create_array(active_rates.description)

		comments = Comment.objects.all() #Retornando los comentarios hechos por los usuarios
		return render(request, self.template_name)

# Calculadora de precios
class CalculatorView(View):
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


class ProfileView(View):
	template_name  = 'profile.html'

	def get(self, request):
		try:
			profile_user = Profile.objects.get(user=request.user)
			#user = EmployeeProfile.objects.get(profile=profile) VERIFICAR BIEN ESTE PEO RECUERDATE YBRAHIN
		except (Profile.DoesNotExist) as e: #ESTA MIERDA SIGUE DANDO PEOS
			return JsonResponse({"response": "Error"})

		return render(request, self.template_name,{"profile":profile_user})
		
	# Registro de clientes
	def post(self, request):
		sign_up	= SignUpForm(request.POST, request.FILES)
		
		response = json.loads(create_user(sign_up,request.POST['avatar']))
		if response['profile'] is None:
			return JsonResponse({"response": response['message']})
		print 'aqui jodo todo'
		profile = serializers.deserialize("json", response['profile']).next().object

		# Asignando grupo:
		group = Group.objects.get(name='clients')
		profile.user.groups.add(group)
		template_name = 'index.html'
		send_email(sign_up.cleaned_data['email'],"Cuenta Creada",sign_up.cleaned_data) #Enviando correo

		return HttpResponseRedirect('/')


	def put(self,request):
		print "actualizar cuenta"

	@permission_required('app.change_employeeprofile')
	def delete(self,request):
		print "deshabilitar cuenta"

# Registro de empleados
@login_required
class EmployeeView(View):
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
class AdminView(View):
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
class AgencyView(View):
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
class RateView(View):
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
#@login_required
class ShipmentView(View):

	template_name = 'shipments.html'
	def get(self, request):
		return render(request, self.template_name)

	#@permission_required('app.add_shipment')
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
class PackageView(View):
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
class CommentView(View):
	@permission_required('app.add_comment')
	def post(self, request):
		new_comment = CommentForm(request.POST, request.FILES)

		if not new_comment.is_valid():
			return JsonResponse({"response": "Error"})

		data = new_package.cleaned_data
		comment = Comment(user=request.user, comment=data['comment'])
		comment.save()

		return JsonResponse({"response": "ok"})
		
#Dashboard
#@login_required(login_url='app:login')
class DashboardView(View):
	template_name = 'dashboard.html'

	def get(self, request):

		try:
			profile_user = Profile.objects.get(user=request.user)
			#user = EmployeeProfile.objects.get(profile=profile) VERIFICAR BIEN ESTE PEO RECUERDATE YBRAHIN
		except (Profile.DoesNotExist) as e: #ESTA MIERDA SIGUE DANDO PEOS
			return JsonResponse({"response": "Error"})

		if request.user.is_employee():
			try:
				profile_user_employee = EmployeeProfile.get(profile = profile_user)
			except (EmployeeProfile.DoesNotExist) as e:
				return JsonResponse({"response": "Error"})

		if request.user.is_manager:
			try:
				agency_managment = Agency.get(manager=request.user)
			except (Agency.DoesNotExist) as e:
				return JsonResponse({"response": "Error"})

			employees_agency = 	EmployeeProfile.objects.filter(agency=agency_managment, is_active=True) #Empleados de una agencia
			shipments_recive = Shipment.objects.filter(agency = agency_managment)
		return render(request, self.template_name)
		#return JsonResponse({"response": "Yeah"})


class ContactView(View):
	def post(self,request):
		
		return JsonResponse({"response":"Yeah"})