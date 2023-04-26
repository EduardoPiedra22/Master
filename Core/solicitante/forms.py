from django import forms
from django.forms import ModelChoiceField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import*

class SolicitanteForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('tipo_documento', css_class='form-group col-md-2'),
				Column('cedula', css_class='form-group col-md-10'),
				Column('nombre', css_class='form-group col-md-6'),
				Column('apellido', css_class='form-group col-md-6'),
				Column('fecha_nacimiento', css_class='form-group col-md-4'),
				Column('edad', css_class='form-group col-md-4'),
				Column('sexo', css_class='form-group col-md-4'),
				Column('telefono', css_class='form-group col-md-4'),
				Column('correo_electronico', css_class='form-group col-md-8'),
				Column('direccion', css_class='form-group col-md-12'),

				css_class='form-row'
				),
			)

	class Meta:
		model = Solicitante
		fields = 'tipo_documento', 'cedula', 'nombre', 'apellido','fecha_nacimiento', 'edad','sexo', 'telefono', 'correo_electronico', 'direccion','fecha_registro', 'fecha_actulizacion', 'user_creation','user_update'
		exclude =['fecha_registro','fecha_actulizacion','user_creation','user_update']
		widgets = {
			'tipo_documento':forms.Select(
	        	attrs = {
	        		'class': 'form-control',
	        	}),

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

	        'correo_electronico':forms.EmailInput(
	        	attrs = {
	        		'class': 'form-control',
	        		'placeholder':'Introduce correo electronico'
	        	}),

            'direccion':forms.Textarea(
            	attrs={
            		'class':'form-control mt-3',
            		'rows': 3,
            		'cols': 3,
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

"""	def clean_cedula(self):

		Valída que sea Correcta la Cédula

		ced = self.cleaned_data['cedula']
		msg = "La Cédula introducida no es válida"
		valores = [ int(ced[x]) * (2 - x % 2) for x in range(7) ]
		suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
		veri = 10 - (suma - (10 * (suma / 10)))
		if int(ced[7]) == int(str(veri)[-1:]):
			return ced
		else:
			raise forms.ValidationError(msg)
"""
"""
			
			class SolicitanteForm2(forms.ModelForm):
				class Meta:
					model = Solicitante
					fields = ('__all__')
					widgets = {
						'fecha_registro':forms.DateInput(),
						'cedula':forms.TextInput(),
						'nombre':forms.TextInput(),
						'apellido':forms.TextInput(),
						'telefono':forms.TextInput(),
						'correo_electronico':forms.EmailInput(),
						'direccion':forms.TextInput(),
						}
			
			"""			
"""
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
		return data"""

"""
class MunicipioForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('nombre', css_class='form-group col-md-12'),
				css_class='form-row'
				)
			)

	class Meta:
		model = Municipio
		fields = '__all__'
		labels = {'nombre':'Municipio'}
		widgets = {
			'nombre':forms.TextInput(
				attrs = {
					'class': 'form-control',
					'placeholder':'Introduce el nombre'
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

class ParroquiaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('id_municipio', css_class='form-group col-md-12'),
				css_class='form-row'
				),
			Row(
				Column('nombre', css_class='form-group col-md-12'),
				css_class='form-row'
				),
			)
			
	class Meta:
		model = Parroquia
		fields = '__all__'
		labels = {'nombre':'Parroquia', 'id_municipio':'Municipio'}

		widgets = {
			'id_municipio':forms.Select(attrs={'class':'form-control'}),
			'nombre':forms.TextInput(attrs = {'class': 'form-control','placeholder':'Introduce el nombre'}),
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



class ComunaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('id_municipio', css_class='form-group col-md-12'),
				css_class='form-row'
				),
			Row(
				Column('id_parroquia', css_class='form-group col-md-12'),
				css_class='form-row'
				),
			Row(
				Column('nombre', css_class='form-group col-md-12'),
				css_class='form-row'
				),
			)
	class Meta:
		model = Comuna
		fields = '__all__'
		labels = {'nombre':'Comuna', 'id_municipio':'Municipios', 'id_parroquia':'Parroquias'}
		widgets = {
			'id_municipio':forms.Select(attrs={'class':'form-control'}),
			'id_parroquia':forms.Select(attrs={'class':'form-control'}),
			'nombre':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Introduce el nombre' })
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


class FormularioSelectorDireccion(forms.Form):
    municipios = ModelChoiceField(queryset=Municipio.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    parroquias = ModelChoiceField(queryset=Parroquia.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    comunas = ModelChoiceField(queryset=Comuna.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


    def __init__(self, *args, **kwargs):
        super(FormularioSelectorDireccion, self).__init__(*args, **kwargs)
        self.fields['parroquias'].queryset = Municipio.objects.none()
        self.fields['comunas'].queryset = Municipio.objects.none()

        """