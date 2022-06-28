from dataclasses import field
import email
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cards, Usuarios

class FormularioRegister(UserCreationForm):
    cumpleaños = forms.DateField(input_formats=('%d-%m-%Y','%Y-%m-%d'))
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    
    class Meta:
        model = User
        fields = ['username','password1', 'password2','email', 'first_name', 'last_name']
    
class FormularioEditarPerfil(forms.Form):
    cumpleaños = forms.DateField()
    perfil = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

