# Generated by Django 4.2.6 on 2023-12-06 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_infomiembros_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rhpcconductasaseguir',
            name='id_asesoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.hpc'),
        ),
    ]
