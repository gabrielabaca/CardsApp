# Generated by Django 4.0.4 on 2022-06-15 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_App', '0003_alter_cards_categoria_alter_usuarios_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorias_cards',
            name='descripcion',
            field=models.CharField(default='NONE', max_length=40),
        ),
    ]
