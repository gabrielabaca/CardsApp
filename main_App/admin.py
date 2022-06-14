from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Usuarios)
admin.site.register(Cards)
admin.site.register(Relacion_Cards)
admin.site.register(Perfil_Links)
admin.site.register(Categorias_Cards)