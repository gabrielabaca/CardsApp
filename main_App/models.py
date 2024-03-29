from django.conf import settings
from django.db import models

# Create your models here.

class Usuarios(models.Model):
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cumpleaños = models.DateField(null=True)
    avatar = models.ImageField(upload_to='Avatares/', null = True, blank = True)
    perfil = models.TextField(null=True)
    links = models.IntegerField(null = True)
    estado = models.IntegerField(null=True)


class Cards(models.Model):
    titulo = models.CharField(max_length=120)
    icon = models.CharField(max_length=20)
    texto = models.TextField()
    imagen = models.ImageField(upload_to='Cards/', null = True, blank = True)
    categoria = models.IntegerField(null = True)
    estado = models.IntegerField()
    creacion = models.DateTimeField(auto_now=True)
    
class Relacion_Cards(models.Model):
    id_card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    id_usr = models.IntegerField()
    id_usr_to = models.IntegerField()

class Perfil_Links(models.Model):
    id_usr = models.IntegerField()
    link = models.CharField(max_length=40)
    icon = models.CharField(max_length=22)

class Categorias_Cards(models.Model):
    id_card = models.IntegerField()
    id_categoria = models.IntegerField()
    descripcion = models.CharField(max_length=40, default='NONE')