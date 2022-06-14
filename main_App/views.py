from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import UserManager, User
from main_App.forms import FormularioRegister
from .models import Usuarios
# Create your views here.

def ingresar(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  
        if user is not None:
            login(request, user)
            return render(request, 'auth/login.html', {'login':True})
        else:
            return render(request, 'auth/login.html', {'login':False, 'mensaje':'Usuario o Contraseña Incorrectos'})
     
    return render(request, 'auth/login.html')


def register(request):
    
    if request.POST:

        if User.objects.filter(username=request.POST["username"]):
            return render(request, 'auth/register.html', {'mensaje': f'El usuario <b>{request.POST["username"]}</b> ya existe'})
        elif User.objects.filter(email = request.POST['email']):
            return render(request, 'auth/register.html', {'mensaje': f'El mail <b>{request.POST["email"]}</b> ya esta en uso'})

        formulario = FormularioRegister(request.POST)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            user=User.objects.create_user(datos['username'],datos['email'],datos['password2'])
            user.last_name=datos['last_name']
            user.first_name=datos['first_name']
            user.save()

            usuario = Usuarios(
                id_usuario=user,
                cumpleaños=datos['cumpleaños'],
                estado=1)
            usuario.save()
            return render(request, 'auth/register.html', {'datos':user})
        else:
            return render(request, 'auth/register.html', {'mensaje':formulario.error_messages})
    else:
        
        return render(request, 'auth/register.html')

def lostpswd(request):
    return render(request, 'auth/lostpswd.html')