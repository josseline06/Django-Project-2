from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.contrib.auth.decorators import permission_required, login_required
from django.core import serializers
from django.contrib.auth.models import Group
from django.shortcuts import render
from .utils import user as utils, mail
from .models import *
from .forms import *
import json

# Pagina principal -- FALTA
class Index(View):
	template_name = 'index.html'
	def get(self, request):
		# Retornando todos los planes de tarifas activos
		active_rates = Rate.objects.filter(is_active=True)

		if active_rates.count() > 0:
			for rate in active_rates:
				rate.description = rate.description.split(',')

		# Retornando los comentarios hechos por los usuarios
		comments_users = Comment.objects.all()
		return render(request, self.template_name,{"rates":active_rates,"comments":comments_users})


# Error 404 
class Error(TemplateView):
	template_name = '404.html'


# Calculadora de precios
class CalculatorView(View):

	def post(self, request, rate):
		try:
			selected_rate = Rate.objects.get(key_name=rate)
		except Rate.DoesNotExist:
			return HttpResponseRedirect('/404')
		
		calculator = CalculatorForm(request.POST, request.FILES)
		if not calculator.is_valid():
			return JsonResponse({"response": "Some of the data is invalid, try again."},status=400)
		data = calculator.cleaned_data
		total = utils.package_cost(selected_rate, data['width'], data['height'], data['depth'], data['weight'], data['price'])
		return JsonResponse({"response": total},status=200)


class ProfileView(View):
	template_name = 'profile.html'

	# Ver perfil de cliente/empleado/administrador
	#@login_required
	def get(self, request):

		try:
			profile = Profile.objects.get(user=request.user)
			agency = None

			if request.user.is_employee():
				employee = EmployeeProfile.objects.get(profile=profile)
				agency = employee.agency

			if request.user.is_manager():
				agency = Agency.objects.get(manager=request.user)
		except (Profile.DoesNotExist, EmployeeProfile.DoesNotExist, Agency.DoesNotExist) as e:
			return HttpResponseRedirect('/404')


		return render(request, self.template_name, {"profile": profile, "agency": agency})
		
	# Registro de clientes
	def post(self, request):
		sign_up	= SignUpForm(request.POST, request.FILES)
		
		response = json.loads(utils.create_user(sign_up,request.POST['avatar']))
		if response['profile'] is None:
			return JsonResponse({"code": 400, "response": response['message']})
		profile = serializers.deserialize("json", response['profile']).next().object

		# Asignando grupo:
		group = Group.objects.get(name='clients')
		profile.user.groups.add(group)
		# MEJORAR 
		mail.send_email(sign_up.cleaned_data['email'],"Cuenta Creada",sign_up.cleaned_data,'welcome') #Enviando correo

		return HttpResponseRedirect('/')

	# Editar perfil de cliente/empleado/administrador
	@login_required
	def put(self, request):
		profile = ProfileForm(request.POST, request.FILES)

		if not profile.is_valid():
			return JsonResponse({"code": 400, "response": "Some of the data is invalid, try again."})
		
		data = profile.cleaned_data
		avatar = None
		
		# Si edita correo:
		if request.user.email != data['email']:
			try:
				user = User.objects.get(email=data['email'])
				return JsonResponse({"code": 400, "response": "This email already exists, try again."})
			except User.DoesNotExist:
				request.user.email = data['email']
				# Deberia mandar un correo de que se cambio
				if request.user.avatar:
					avatar = request.user.avatar
				elif utils.gravatar_avatar(request.user):
					request.user.social_avatar = utils.create_gravatar(request.user.email)

		# Si edita avatar:
		if data['avatar']:
			avatar = data['avatar']

		# Si hay algun cambio en el correo o el avatar
		if avatar:
			request.user.avatar = avatar

		request.user.phone = data['phone']
		request.user.location = utils.create_location(data['address'], data['postal_code'], data['city'], data['country'])
		request.user.save()

		return JsonResponse({"code": 200, "response": "Your profile has been changed successfully."})


@login_required
class EmployeeView(View):
	# Lista de empleados de una agencia
	def get(self, request):
		print "llego :D"

	# Registro de empleados
	@permission_required('app.add_employeeprofile')
	def post(self, request):
		new_employee = EmployeeForm(request.POST, request.FILES)
		
		response = json.loads(utils.create_user(new_employee, request.POST['avatar']))
		if response['profile'] is None:
			return JsonResponse({"code": 400, "response": response['message']})
		profile = serializers.deserialize("json", response['profile']).next().object

		# Agregando agencia:
		employee = EmployeeProfile(profile=profile, agency=new_employee.cleaned_data['agency'])
		employee.save()
		# Asignando grupo:
		group = Group.objects.get(name='employees')
		profile.user.groups.add(group)

		# Enviar correo a gerente y a empleado

		return JsonResponse({"code": 201, "response": "The employee has been successfully registered."})


@login_required
class AdminView(View):
	# Lista de gerentes
	def get(self, request):
		print "llego :D"

	# Registro de administradores
	@permission_required('app.add_agency')
	def post(self, request):
		new_admin = AdminForm(request.POST, request.FILES)
		
		response = json.loads(utils.create_user(new_admin, request.POST['avatar']))
		if response['profile'] is None:
			return JsonResponse({"code": 400, "response": response['message']})
		profile = serializers.deserialize("json", response['profile']).next().object

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

		# Enviar correo a nuevo admin y a admin

		return JsonResponse({"code": 200, "response": "The admin has been successfully registered."})


@login_required
class AgencyView(View):
	# Lista de agencias
	def get(self, request):
		print "llego :D"

	# Registro de agencias
	@permission_required('app.add_agency')
	def post(self, request):
		new_agency = AgencyForm(request.POST, request.FILES)

		if not new_agency.is_valid():
			return JsonResponse({"code": 400, "response": "Some of the data is invalid, try again."})

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

				#Enviar email a admin

				return JsonResponse({"code": 201, "response": "The agency has been successfully registered."})

			return JsonResponse({"code": 400, "response": "An agency already exists in that address."})
		return JsonResponse({"code": 400, "response": "An agency already exists in that name."})


# Registro de tarifas
@login_required
class RateView(View):
	# Lista de tarifas
	def get(self, request):
		print "llego :D"

	@permission_required('app.add_rate')
	def post(self, request):
		new_rate = RateForm(request.POST, request.FILES)

		if not new_rate.is_valid():
			return JsonResponse({"code": 400, "response": "Some of the data is invalid, try again."})

		# Agregando nueva tarifa:
		data = new_rate.cleaned_data
		key_name = utils.create_key_name(data['name'])
		try:
			rate = Rate.objects.get(key_name=key_name)
		except Rate.DoesNotExist:
			try:
				rate = Rate.objects.get(value=data['value'], percent=data['percent'])
			except Rate.DoesNotExist:
				rate = Rate(key_name=key_name, name=data['name'], value=data['value'], percent=data['percent'], description=data['description'])
				rate.save()

				# Enviar email a admin
				
				return JsonResponse({"code": 201, "response": "The rate has been successfully registered."})
			return JsonResponse({"code": 400, "response": "An rate already exists with those values."})
		return JsonResponse({"code": 400, "response": "An rate already exists with this name."})


#@login_required
class ShipmentView(View):
	template_name = 'shipments.html'
	
	def get(self, request):
		return render(request, self.template_name)

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

		#try:
		#	profile_user = Profile.objects.get(user=request.user)
			#user = EmployeeProfile.objects.get(profile=profile) VERIFICAR BIEN ESTE PEO RECUERDATE YBRAHIN
		#except (Profile.DoesNotExist) as e: #ESTA MIERDA SIGUE DANDO PEOS
		#	return JsonResponse({"response": "Error 1"})

		if request.user.is_employee():
			try:
				profile_user_employee = EmployeeProfile.objects.get(profile = profile_user)
			except (EmployeeProfile.DoesNotExist) as e:
				return JsonResponse({"response": "Error 2"})

		if request.user.is_manager:
			try:
				agency_managment = Agency.objects.get(manager=request.user)
			except (Agency.DoesNotExist) as e:
				return JsonResponse({"response": "Error 3"})

			employees_agency = 	EmployeeProfile.objects.filter(agency=agency_managment) #Empleados de una agencia
			shipments_recive = Shipment.objects.filter(agency = agency_managment)
		return render(request, self.template_name)
		#return JsonResponse({"response": "Yeah"})


class ContactView(View):
	def post(self,request):
		
		return JsonResponse({"response":"Yeah"})


