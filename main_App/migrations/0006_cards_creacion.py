# Generated by Django 4.0.4 on 2022-06-16 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_App', '0005_alter_relacion_cards_id_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='cards',
            name='creacion',
            field=models.DateTimeField(auto_now=True),
        ),
    ]