# Generated by Django 4.0.4 on 2022-06-16 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_App', '0004_categorias_cards_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relacion_cards',
            name='id_card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_App.cards'),
        ),
    ]
