from django.conf.urls import url
import views

urlpatterns = [
    # Pagina principal
    url(r'^index/$', views.Index.as_view(), name='index'),
    url(r'^$', views.Index.as_view(), name='index'),
    
    # Calculadora
    url(r'^calculator/rates/(?P<rate>\w+)/$', views.CalculatorView.as_view(), name='calculator'),

    # Login
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),

    # Logout
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    # Views Cliente - Registrar/Ver/Actualizar/Deshabilitar
    url(r'^sign_up/$', views.ProfileView.as_view(), name='sign_up'),
    url(r'^me/$', views.ProfileView.as_view(), name='profile'),
    url(r'^me/edit/$', views.ProfileView.as_view(), name='edit_profile'),
    url(r'^me/delete/$', views.ProfileView.as_view(), name='delete_profile'),

     # Dashboard
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),

    # History
    url(r'^history/$', views.DashboardView.as_view(), name='history'),

    #Contacts
    url(r'^contact/$',views.ContactView.as_view(),name='contacts'),

    url(r'^shipment/$', views.ShipmentView.as_view(), name='shipment'),
    
    # Error 404
    url(r'^404/$', views.Error.as_view(), name='error'), 

]