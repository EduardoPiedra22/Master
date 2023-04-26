# Generated by Django 4.0.4 on 2022-11-22 16:01

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
            name='Solicitante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('tipo_documento', models.CharField(choices=[('VENEZOLANO', 'V'), ('EXTRANJERO', 'E'), ('PASAPORTE', 'P')], default='V', max_length=45, verbose_name='Tipo de documento')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, null=True)),
                ('fecha_actulizacion', models.DateTimeField(auto_now=True, null=True)),
                ('cedula', models.CharField(max_length=10, unique=True, verbose_name='Cedula')),
                ('nombre', models.CharField(max_length=25, verbose_name='Nombres')),
                ('apellido', models.CharField(max_length=25, verbose_name='Apellido')),
                ('telefono', models.CharField(max_length=30, verbose_name='Telefono')),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('direccion', models.CharField(blank=True, max_length=150, null=True, verbose_name='Dirección')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('edad', models.IntegerField()),
                ('sexo', models.CharField(choices=[('M', 'MASCULINO'), ('F', 'FEMENINO')], default='M', max_length=10, verbose_name='Sexo')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_creation', to=settings.AUTH_USER_MODEL)),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_update', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Solicitante',
                'verbose_name_plural': 'Solicitantes',
                'db_table': 'Solicitantes',
                'ordering': ['id'],
            },
        ),
    ]
