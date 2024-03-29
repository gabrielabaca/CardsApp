# Generated by Django 4.0.5 on 2022-06-10 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=120)),
                ('icon', models.CharField(max_length=20)),
                ('texto', models.TextField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='Cards')),
                ('categoria', models.IntegerField()),
                ('estado', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Categorias_Cards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_card', models.IntegerField()),
                ('id_categoria', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Perfil_Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_usr', models.IntegerField()),
                ('link', models.CharField(max_length=40)),
                ('icon', models.CharField(max_length=22)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cumpleaños', models.DateField()),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='Avatares')),
                ('perfil', models.TextField()),
                ('links', models.IntegerField()),
                ('estado', models.IntegerField()),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Relacion_Cards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_usr', models.IntegerField()),
                ('id_usr_to', models.IntegerField()),
                ('id_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_App.usuarios')),
            ],
        ),
    ]
