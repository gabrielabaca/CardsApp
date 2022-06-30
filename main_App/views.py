import django
import platform
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from main_App.forms import FormularioRegister, FormularioEditarPerfil
from .models import Usuarios, Perfil_Links, Cards, Categorias_Cards, Relacion_Cards


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

    left = True
    cards = []
    i=0
    
    if(request.GET):
        #Recibidas
        if request.GET['action'] == 'recibidas':
            for x in Relacion_Cards.objects.filter(id_usr_to__iexact = request.user.id).order_by('-id'):
                cards.append({i:{}})
                dates = timezone.now() - x.id_card.creacion
                cards[i].update({
                    'id': x.id_card.id,
                    'titulo':x.id_card.titulo,
                    'icon':x.id_card.icon,
                    'text':x.id_card.texto,
                    'imagen':x.id_card.imagen,
                    'estado':x.id_card.estado,
                    'left': (True if left else False),
                    'categoria':[],
                    'id_prop': User.objects.get(id=x.id_usr),
                    'id_to': User.objects.get(id=x.id_usr_to),
                    'creacion': f'{dates.days} dias'
                })
                left = (False if left else True)
                for y in Categorias_Cards.objects.filter(id_card=x.id_card.id):
                    cards[i]['categoria'].append(y.descripcion)
                i += 1
            return render(request, 'main/cards.html',{'datos':datosUsuario, 'perfilCards':perfilcards, 'links': links, 'cards':cards, 'cardsTitulo':'Tarjetas Recibidas'})
        
        #Enviadas
        if (request.GET['action'] == 'enviadas'):
            for x in Relacion_Cards.objects.filter(id_usr__iexact = request.user.id).order_by('-id'):
                cards.append({i:{}})
                dates = timezone.now() - x.id_card.creacion
                cards[i].update({
                    'id': x.id_card.id,
                    'titulo':x.id_card.titulo,
                    'icon':x.id_card.icon,
                    'text':x.id_card.texto,
                    'imagen':x.id_card.imagen,
                    'estado':x.id_card.estado,
                    'left': (True if left else False),
                    'categoria':[],
                    'id_prop': User.objects.get(id=x.id_usr),
                    'id_to': User.objects.get(id=x.id_usr_to),
                    'creacion': f'{dates.days} dias'
                })
                left = (False if left else True)
                for y in Categorias_Cards.objects.filter(id_card=x.id_card.id):
                    cards[i]['categoria'].append(y.descripcion)
                i += 1
            return render(request, 'main/cards.html',{'datos':datosUsuario, 'perfilCards':perfilcards, 'links': links, 'cards':cards, 'cardsTitulo':'Tarjetas Enviadas'})
        
    #Todas las tarjetas
    
    for x in Cards.objects.all().order_by('-id'):
        cards.append({i:{}})
        dates = timezone.now() - x.creacion
        cards[i].update({
            'id': x.id,
            'titulo':x.titulo,
            'icon':x.icon,
            'text':x.texto,
            'imagen':x.imagen,
            'estado':x.estado,
            'left': (True if left else False),
            'categoria':[],
            'id_prop': User.objects.get(id=(Relacion_Cards.objects.get(id_card=x.id).id_usr)),
            'id_to': User.objects.get(id=(Relacion_Cards.objects.get(id_card=x.id).id_usr_to)),
            'creacion': f'{dates.days} dias'
        })
        left = (False if left else True)
        for y in Categorias_Cards.objects.filter(id_card=x.id):
            cards[i]['categoria'].append(y.descripcion)
        i += 1
    return render(request, 'main/cards.html',{'datos':datosUsuario, 'perfilCards':perfilcards, 'links': links, 'cards':cards, 'cardsTitulo':'Todas las tarjetas'})


@login_required(login_url='ingresar')
def nuevaCard(request):

    if request.POST:
        faicon = ''
        categoria = ''
        privada = 0
        if request.POST['card-categoria'] == '1' :
            faicon = 'fa-cake-candles'
            categoria = 'Aniversario'
        if request.POST['card-categoria'] == '2' :
            faicon = 'fa-cake-candles'
            categoria = 'Cumpleaños'
        elif request.POST['card-categoria'] == '3' :
            faicon = 'fa-graduation-cap'
            categoria = 'Estudiantes'
        elif request.POST['card-categoria'] == '4' :
            faicon = 'fa-heart'
            categoria = 'SanValentin'
        if request.POST == 'card-privada':
            privada = 2

        card = Cards(
            titulo = request.POST['card-titulo'],
            icon = faicon,
            texto = request.POST['card-mensaje'],
            categoria = request.POST['card-categoria'],
            estado = privada,
            )
        
        card.save()
        rCard = Relacion_Cards(
            id_card = card,
            id_usr = request.user.id,
            id_usr_to = request.POST['card-id-to'],
        )
        rCard.save()

        cCard = Categorias_Cards(
            id_card = card.id,
            id_categoria = card.categoria,
            descripcion = categoria,
        )

        cCard.save()
        return redirect(dashboard)
        
@login_required(login_url='ingresar')
def imagenPerfil(request):
    if request.POST:
        
        usuario = Usuarios.objects.get(id_usuario = request.user.id)
        nuevaImagen = Usuarios(
            id = usuario.id, 
            id_usuario = request.user, 
            avatar = request.FILES['nuevaImagen'],
            cumpleaños = usuario.cumpleaños,
            perfil = usuario.perfil,
            links = usuario.links,
            estado = usuario.estado)

        nuevaImagen.save()
        return redirect(dashboard)

@login_required(login_url='ingresar')
def editarPerfil(request):
    #Perfil de usuario
    datosUsuario = Usuarios.objects.get(id_usuario=request.user.id)
    perfilcards = ({
        'enviadas' : len(Relacion_Cards.objects.filter(id_usr__iexact = request.user.id)), 
        'recibidas': len(Relacion_Cards.objects.filter(id_usr_to__iexact = request.user.id)),
        })

    links = Perfil_Links.objects.filter(id_usr = request.user.id)

    if request.POST:
        if request.POST['btnPerfil']:
            formulario = FormularioEditarPerfil(request.POST)
            if formulario.is_valid():
                datos = formulario.cleaned_data
                print(formulario)
                usuario = Usuarios.objects.get(id_usuario = request.user.id)
                editarPerfil = Usuarios(
                id = usuario.id, 
                id_usuario = request.user, 
                avatar = usuario.avatar,
                cumpleaños = datos['cumpleaños'],
                perfil = datos['perfil'],
                links = usuario.links,
                estado = usuario.estado)
                editarPerfil.save()

                changeUser = User.objects.get(pk=request.user.id)
                changeUser.email = datos['email']
                changeUser.first_name = datos['first_name']
                changeUser.last_name = datos['last_name']

                changeUser.save()

                return render(request, 'main/editarperfil.html', {'datos':datosUsuario, 'perfilCards':perfilcards, 'success':True})

            else:
                return render(request, 'main/editarperfil.html', {'datos':datosUsuario, 'perfilCards':perfilcards, 'error':'Por favor revisa los datos ingresados'})
        
        elif request.POST['password1']:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.get(pk = request.user.id)

                user.set_password(request.POST['password1'])
                user.save()
                return render(request, 'main/editarperfil.html', {'datos':datosUsuario, 'perfilCards':perfilcards, 'error':'Se cambio la contraseña'})
            else:
                return render(request, 'main/editarperfil.html', {'datos':datosUsuario, 'perfilCards':perfilcards, 'error':'Las contraseñas no coinciden'})
            

    return render(request, 'main/editarperfil.html', {'datos':datosUsuario, 'perfilCards':perfilcards,'links':links})


def about(request):

    return render(request,'main/about.html',{'django_version':django.VERSION[0:3], 'python_version': platform.python_version})

##JSONS
@login_required(login_url='ingresar')
def getUsers(request):

    users = {'usersList':[]}
    for x in User.objects.all().exclude(id = request.user.id):
        users['usersList'].append({'id':x.id, 'username':x.username, 'email':x.email})

    return JsonResponse(users)


@login_required(login_url='ingresar')
def getRandon(request):

    cards = {}
    data = Relacion_Cards.objects.order_by('?').first()
    dates = timezone.now() - data.id_card.creacion
    cards.update({
        'id': data.id_card.id,
        'titulo':data.id_card.titulo,
        'icon': data.id_card.icon,
        'text': data.id_card.texto,
        #'imagen': data.id_card.imagen.url,
        'estado': data.id_card.estado,
        'left': (True if data.id % 2 == 1 else False),
        'categoria':[],
        'id_prop': (User.objects.get(id=data.id_usr).username if data.id_card.estado != 2 else 'Privado'),
        'id_to': (User.objects.get(id=data.id_usr_to).username if data.id_card.estado != 2 else 'Privado'),
        'creacion': f'{dates.days} dias'
    })
    for y in Categorias_Cards.objects.filter(id_card=data.id_card.id):
        cards['categoria'].append(y.descripcion)
    
    return JsonResponse(cards)