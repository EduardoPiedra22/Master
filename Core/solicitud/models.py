from django.db import models
from datetime import datetime
from crum import get_current_user

from django.forms import model_to_dict

from Core.solicitante.models import Solicitante
from Core.solicitud.choices import *

from django.conf import settings
# Create your models here.


class BaseModel(models.Model):
	user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_creation', null=True, blank=True)
	date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	user_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_update', null=True, blank=True)
	date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

	class Meta:
		verbose_name = "Basemodel"
		verbose_name_plural = "basemodels"
		db_table = 'user'

class Categorias(BaseModel):
	nombre = models.CharField(max_length=25, verbose_name='Nombre', unique=True)
	descipcion = models.CharField(max_length=250, null=False, blank=False, verbose_name='Descripcion')

	class Meta:
		verbose_name = "Categorias"
		verbose_name_plural = "Categorias"
		db_table = 'Categoria_Solicitud'

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		user = get_current_user()
		if user is not None:
			if not self.pk:
				self.user_creation = user
			else:
				self.user_update = user
			super(Categorias, self).save()
	
	def toJSON(self):
		item = model_to_dict(self)
		return item

	def __str__(self):
		return str(self.nombre)


class Solicitudes(models.Model):
	fecha_registro = models.DateField(auto_now_add=True)
	categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, verbose_name='Categoria')
	id_solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE, verbose_name= 'Solicitante')
	estatus = models.CharField(max_length=9, choices=aprobado_choices, default='ESPERA',null=True, blank=True, verbose_name='Estatus')
	descripcion = models.CharField(max_length=250, null=False, blank=False, verbose_name='Descripcion')
	descripcion_motivo = models.CharField(max_length=250, null=True, blank=True, verbose_name='Descripcion')


	def toJSON(self):
		item = model_to_dict(self)
		item['fecha_registro'] = self.fecha_registro.strftime('%Y-%m-%d')
		item['categoria'] = self.categoria.toJSON()
		item['id_solicitante'] = self.id_solicitante.toJSON()
		return item

	def __str__(self):
		return '{} {} {}'.format(self.id, self.id_solicitante, self.estatus)





class EncargadoBaseMisiones(models.Model):
	cedula = models.CharField(max_length=10, unique=True, verbose_name='Cedula')
	fecha_nacimiento = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Fecha de nacimiento')
	nombre = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nombres')
	apellido = models.CharField(max_length=50, null=False, blank=False, verbose_name='Apellidos')
	edad = models.IntegerField()
	sexo = models.CharField(max_length=10, choices=sexo, default='M',null=False, blank=False, verbose_name='Sexo')
	email = models.EmailField(unique=True)
	telefono = models.CharField(max_length=30, null=False, blank=False, verbose_name='Telefono')
	codigo = models.CharField(max_length=9, unique=True, blank=False, null=False, verbose_name='Codigo')
	serial = models.CharField(max_length=9, unique=True, blank=False, null=False, verbose_name='Serial')

	def __str__(self):
		return self.get_full_name()

	def get_full_name(self):
		return '{} / {} {}'.format(self.cedula, self.apellido, self.nombre)


	def toJSON(self):
		item = model_to_dict(self)
		item['full_name'] = self.get_full_name()
		item['full_person'] = '{} / {} / {}'.format(self.fecha_nacimiento.strftime('%Y-%m-%d'), self.edad, self.sexo)
		item['full_contact'] = '{} / {}'.format(self.telefono, self.email)
		item['datos_patria'] = '{} / {}'.format(self.codigo, self.serial)
		return item



	class Meta:
		verbose_name = 'Encargado'
		verbose_name_plural = 'Encargados'
		db_table='Encargados'
		ordering = ['id']




class BaseGrandesMisiones(models.Model):
	nombre = models.CharField(max_length=25, verbose_name='Nombre de la Base de Misiones', unique=True)
	responsable = models.ForeignKey(EncargadoBaseMisiones, on_delete=models.CASCADE, verbose_name='Encargado o Responsable')
	municipio = models.CharField(max_length=100, choices=municipios, default='GUANARE',null=False, blank=False, verbose_name='Municipios')
	nombre_p = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nombre de la Parroquia')
	nombre_c = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nombre de la Comunidad')


	def __str__(self):
		return self.nombre


	def toJSON(self):
		item = model_to_dict(self)
		item['responsable'] = self.responsable.toJSON()
		return item

	class Meta:
		verbose_name = 'Base_de_Misiones_y_Grandes_Misiones'
		verbose_name_plural = 'Base_de_Misiones_y_Grandes_Misiones'
		db_table='Misiones_y_Grandes_Misiones'
		ordering = ['id']



