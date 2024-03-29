from django.urls import path
from main_App import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.ingresar),
    path('ingresar', views.ingresar, name='ingresar'),
    path('register', views.register, name='register'),
    path('lostpswd', views.lostpswd, name='lostpswd'),
    path('logout', LogoutView.as_view(), name= 'logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('editarPerfil', views.editarPerfil),
    path('nuevaCard', views.nuevaCard),
    path('imagenPerfil', views.imagenPerfil),
    path('about', views.about, name='about'),
    ## JSONS
    path('getUsers', views.getUsers),
    path('getCard', views.getRandon),
]
