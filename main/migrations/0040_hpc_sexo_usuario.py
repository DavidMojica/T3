# Generated by Django 4.2.6 on 2023-12-31 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_alter_psillamadas_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='hpc',
            name='sexo_usuario',
            field=models.ForeignKey(default=django.db.models.deletion.SET_NULL, on_delete=django.db.models.deletion.CASCADE, to='main.sexo'),
        ),
    ]
