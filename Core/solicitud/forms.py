from datetime import datetime

from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import *

class CategoriasForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('nombre', css_class='form-group col-md-6'),
				Column('descipcion', css_class='form-group col-md-6'),
				css_class='form-row'
				),
			)

	class Meta:
		model = Categorias
		fields = '__all__'
		widgets = {
		'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce tipo de ayuda'}),
		'descipcion':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce descripcion de ayuda'}),
		}
		exclude =['user_creation','user_update']


	def save(self):
		data = {}
		form = super()
		try:
			if form.is_valid():
				form.save()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data



class SolicitudesForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('categoria', css_class='form-group col-md-6'),
				Column('id_solicitante', css_class='form-group col-md-6'),
				Column('descripcion', css_class='form-group col-md-12'),
				css_class='form-row'
				),
			)

	class Meta:
		model = Solicitudes
		fields = '__all__'
		widgets = {
			'categoria':forms.Select(attrs={'class':'form-control select2 mt-3'}),
			'id_solicitante':forms.Select(attrs={'class':'form-control select2 mt-3'}),
			'descripcion':forms.Textarea(attrs={'class':'form-control mt-3','rows': 3, 'cols': 3}),
		}
		exclude =['user_creation','user_update']
	def save(self):
		data = {}
		form = super()
		try:
			if form.is_valid():
				form.save()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data



class SolicitudesForm2(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('estatus', css_class='form-group col-md-12'),
				Column('descripcion_motivo', css_class='form-group col-md-12'),
				css_class='form-row'
				),
			)

	class Meta:
		model = Solicitudes
		fields = '__all__'
		widgets = {
			'estatus':forms.Select(attrs={'class':'form-control select2 mt-3'}),
			'descripcion_motivo':forms.Textarea(attrs={'class':'form-control mt-3','rows': 3, 'cols': 3}),
		}
		exclude =['id_solicitante','categoria','descripcion','user_creation','user_update']
	def save(self):
		data = {}
		form = super()
		try:
			if form.is_valid():
				form.save()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data




class TestForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=Categorias.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = forms.ModelChoiceField(queryset=Solicitudes.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = forms.ModelChoiceField(queryset=Solicitudes.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


class EncargadoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('cedula', css_class='form-group col-md-4'),
				Column('nombre', css_class='form-group col-md-4'),
				Column('apellido', css_class='form-group col-md-4'),
				Column('fecha_nacimiento', css_class='form-group col-md-4'),
				Column('edad', css_class='form-group col-md-4'),
				Column('sexo', css_class='form-group col-md-4'),
				Column('codigo', css_class='form-group col-md-6'),
				Column('serial', css_class='form-group col-md-6'),
				Column('telefono', css_class='form-group col-md-12'),
				Column('email', css_class='form-group col-md-12'),
				css_class='form-row'
				),
			)

	class Meta:
		model = EncargadoBaseMisiones
		fields = 'cedula', 'nombre', 'apellido','fecha_nacimiento','edad','sexo','telefono','email','codigo', 'serial'
		widgets = {
	        'cedula':forms.TextInput(
	        	attrs = {
	        		'class': 'form-control',
	        		'placeholder':'Introduce tus numero de Cedula'
	        	}),

            'nombre':forms.TextInput(
            	attrs={
            		'class':'form-control',
            		'placeholder':'Introduce tus Nombres'
            	}),

	        'apellido':forms.TextInput(
	        	attrs = {
	        		'class': 'form-control',
	        		'placeholder':'Introduce tus Apellidos'
	        	}),


	        'fecha_nacimiento':forms.DateTimeInput(
	        	attrs = {
	        		'class': 'form-control',
	        		'type':'date',
	        	}),

	        'edad':forms.NumberInput(
	        	attrs = {
	        		'class': 'form-control',
	        		
	        	}),

	        'sexo':forms.Select(
	        	attrs = {
	        		'class': 'form-control select2',
	        		
	        	}),

	        'telefono':forms.TextInput(
	        	attrs = {
	        		'class': 'form-control',
	        		'placeholder':'Telefono fijo o de Casa'
	        	}),

	        'email':forms.EmailInput(
	        	attrs = {
	        		'class': 'form-control',
	        		'placeholder':'Introduce correo electronico'
	        	}),

	        'codigo':forms.NumberInput(
	        	attrs = {
	        	'class': 'form-control',
	        	'placeholder':'Codigo de carnet de la Patria',
	        	'id':'id_codigo'
	        	}),

	        'serial':forms.NumberInput(
	        	attrs = {
	        	'class': 'form-control',
	        	'placeholder':'Serial de carnet de la Patria',
	        	'id':'id_codigo'
	        	}),
        }

	def save(self):
		data = {}
		form = super()
		try:
			if form.is_valid():
				form.save()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data




class BaseMisionesGrandeMisionesForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('nombre', css_class='form-group col-md-4'),
				Column('responsable', css_class='form-group col-md-8'),
				Column('municipio', css_class='form-group col-md-4'),
				Column('nombre_p', css_class='form-group col-md-4'),
				Column('nombre_c', css_class='form-group col-md-4'),
				css_class='form-row'
				),
			)

	class Meta:
		model = BaseGrandesMisiones
		fields = 'nombre','responsable','municipio','nombre_p','nombre_c'
		widgets = {
			'nombre':forms.TextInput(attrs={'class':'form-control'}),
			'responsable':forms.Select(attrs={'class':'form-control select2'}),
			'municipio':forms.Select(attrs={'class':'form-control select2'}),
			'nombre_p':forms.TextInput(attrs={'class':'form-control'}),
			'nombre_c':forms.TextInput(attrs={'class':'form-control'}),
		}
	def save(self):
		data = {}
		form = super()
		try:
			if form.is_valid():
				form.save()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data

