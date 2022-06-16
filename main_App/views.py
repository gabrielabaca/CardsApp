from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from main_App.forms import FormularioRegister
from .models import Usuarios, Perfil_Links, Cards, Categorias_Cards, Relacion_Cards
from datetime import timedelta

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

@login_required(login_url='ingresar')
def dashboard(request):
    #Perfil de usuario
    datosUsuario = Usuarios.objects.get(id_usuario=request.user.id)

    perfilcards = ({
        'enviadas' : len(Relacion_Cards.objects.filter(id_usr__iexact = request.user.id)), 
        'recibidas': len(Relacion_Cards.objects.filter(id_usr_to__iexact = request.user.id)),
        })
    links = Perfil_Links.objects.filter(id_usr = request.user.id)

    cards = []
    i=0
    
    if(request.GET):
        #Recibidas
        if request.GET['action'] == 'recibidas':
            for x in Relacion_Cards.objects.filter(id_usr_to__iexact = request.user.id):
                cards.append({i:{}})
                dates = timezone.now() - x.id_card.creacion
                cards[i].update({
                    'id': x.id_card.id,
                    'titulo':x.id_card.titulo,
                    'icon':x.id_card.icon,
                    'text':x.id_card.texto,
                    'imagen':x.id_card.imagen,
                    'estado':x.id_card.estado,
                    'left': (True if x.id % 2 == 1 else False),
                    'categoria':[],
                    'id_prop': User.objects.get(id=x.id_usr),
                    'id_to': User.objects.get(id=x.id_usr_to),
                    'creacion': f'{dates.days} dias'
                })
                for y in Categorias_Cards.objects.filter(id_card=x.id_card.id):
                    cards[i]['categoria'].append(y.descripcion)
                i += 1
            return render(request, 'main/cards.html',{'datos':datosUsuario, 'perfilCards':perfilcards, 'links': links, 'cards':cards, 'cardsTitulo':'Tarjetas Recibidas'})
        
        #Enviadas
        if (request.GET['action'] == 'enviadas'):
            for x in Relacion_Cards.objects.filter(id_usr__iexact = request.user.id):
                cards.append({i:{}})
                dates = timezone.now() - x.id_card.creacion
                cards[i].update({
                    'id': x.id_card.id,
                    'titulo':x.id_card.titulo,
                    'icon':x.id_card.icon,
                    'text':x.id_card.texto,
                    'imagen':x.id_card.imagen,
                    'estado':x.id_card.estado,
                    'left': (True if x.id % 2 == 1 else False),
                    'categoria':[],
                    'id_prop': User.objects.get(id=x.id_usr),
                    'id_to': User.objects.get(id=x.id_usr_to),
                    'creacion': f'{dates.days} dias'
                })
                for y in Categorias_Cards.objects.filter(id_card=x.id_card.id):
                    cards[i]['categoria'].append(y.descripcion)
                i += 1
            return render(request, 'main/cards.html',{'datos':datosUsuario, 'perfilCards':perfilcards, 'links': links, 'cards':cards, 'cardsTitulo':'Tarjetas Enviadas'})
        
    #Todas las tarjetas
    
    for x in Cards.objects.all():
        cards.append({i:{}})
        dates = timezone.now() - x.creacion
        cards[i].update({
            'id': x.id,
            'titulo':x.titulo,
            'icon':x.icon,
            'text':x.texto,
            'imagen':x.imagen,
            'estado':x.estado,
            'left': (True if x.id % 2 == 1 else False),
            'categoria':[],
            'id_prop': User.objects.get(id=(Relacion_Cards.objects.get(id_card=x.id).id_usr)),
            'id_to': User.objects.get(id=(Relacion_Cards.objects.get(id_card=x.id).id_usr_to)),
            'creacion': f'{dates.days} dias'
        })
        for y in Categorias_Cards.objects.filter(id_card=x.id):
            cards[i]['categoria'].append(y.descripcion)
        i += 1
    return render(request, 'main/cards.html',{'datos':datosUsuario, 'perfilCards':perfilcards, 'links': links, 'cards':cards, 'cardsTitulo':'Todas las tarjetas'})