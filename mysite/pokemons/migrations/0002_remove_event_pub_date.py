# Generated by Django 4.2.5 on 2023-09-30 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='pub_date',
        ),
    ]
