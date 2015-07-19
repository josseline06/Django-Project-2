from django.conf.urls import url
import views

urlpatterns = [
    # Pagina principal
    url(r'^index/', views.Index.as_view(), name='index'),
    url(r'^$', views.Index.as_view(), name='index'),
    
    # Calculadora
    url(r'^calculator/rates/(?P<rate>\w+)/$', views.Calculator.as_view(), name='calculator'),

    # Login
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),

    # Logout
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    # Cliente - Registrar
    url(r'^sign_up/$', views.SignUp.as_view(), name='sign_up'),

    url(r'^shipment/$', views.Shipment.as_view(), name='shipment'),

]