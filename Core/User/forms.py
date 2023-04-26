from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import*

class UserForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('first_name', css_class='form-group col-md-6'),
				Column('last_name', css_class='form-group col-md-6'),
				css_class='form-row'
				),
			Row(
				Column('username', css_class='form-group col-md-4'),
				Column('email', css_class='form-group col-md-8'),
				css_class='form-row'
				),
			Row(
				Column('password', css_class='form-group col-md-8'),
				Column('user_permissions', css_class='form-group col-md-4'),
				css_class='form-row'
				),
			Row(
				Column('groups', css_class='form-group col-md-4'),
				Column('last_login', css_class='form-group col-md-4'),
				Column('date_joined', css_class='form-group col-md-4'),
				css_class='form-row'
				),
			Row(
				Column('is_superuser', css_class='form-group col-md-4'),
				Column('is_staff', css_class='form-group col-md-4'),
				Column('is_active', css_class='form-group col-md-4'),
				Column('imagen', css_class='form-group col-md-12'),
				css_class='form-row'
				),
			
			)

	class Meta:
		model = User
		fields = 'password','last_login','is_superuser','groups','user_permissions','username','first_name','last_name','email','is_staff','is_active','date_joined','imagen'
		widgets = {
			'password':forms.PasswordInput(render_value = True, attrs={'class':'form-control','placeholder':'Introduce tu Password'}),
			'last_login':forms.DateTimeInput(attrs={'type':'date','class':'form-control'}),
			'is_superuser':forms.CheckboxInput(attrs={'type':'checkbox','class':'form-control','style':'font-size: 9px'}),
			'groups':forms.SelectMultiple(attrs={'class':'form-control select2'}),
			'user_permissions':forms.SelectMultiple(attrs={'class':'form-control select2'}),
			'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce tu Username'}),
			'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce tus Nombres'}),
			'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce tus Apellidos'}),
			'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Introduce tu Correo Electronico'}),
			'is_staff':forms.CheckboxInput(attrs={'type':'checkbox','class':'form-control'}),
			'is_active':forms.CheckboxInput(attrs={'type':'checkbox','class':'form-control'}),
			'date_joined':forms.DateTimeInput(attrs={'type':'date','class':'form-control'}),
			'imagen': forms.FileInput(attrs={'placeholder': 'Seleccione Imagen ...',

                }
            ),
		}

	def save(self, commit=True):
		data = {}
		form = super()
		try:
			if form.is_valid():
				pwd = self.cleaned_data['password']
				u = form.save(commit=False)
				if u.pk is None:
					u.set_password(pwd)
				else:
					user = User.objects.get(pk=u.pk)
					if user.password != pwd:
						u.set_password(pwd)
				u.save()
				u.groups.clear()
				for g in self.cleaned_data['groups']:
					u.groups.add(g)
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data




class UserProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('first_name', css_class='form-group col-md-6'),
				Column('last_name', css_class='form-group col-md-6'),
				Column('username', css_class='form-group col-md-12'),
				Column('email', css_class='form-group col-md-12'),
				Column('password', css_class='form-group col-md-12'),
				css_class='form-row'
				),
			)

	class Meta:
		model = User
		fields = 'first_name','last_name','username','email','password','imagen'
		widgets = {
			'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce tus Nombres'}),
			'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce tus Apellidos'}),
			'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce tu Username'}),
			'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Introduce tu Correo Electronico'}),
			'password':forms.PasswordInput(render_value = True, attrs={'class':'form-control','placeholder':'Introduce tu Password'}),
		}
		exclude =['is_superuser','is_staff','is_active','user_permissions','last_login','date_joined','groups']

	def save(self, commit=True):
		data = {}
		form = super()
		try:
			if form.is_valid():
				pwd = self.cleaned_data['password']
				u = form.save(commit=False)
				if u.pk is None:
					u.set_password(pwd)
				else:
					user = User.objects.get(pk=u.pk)
					if user.password != pwd:
						u.set_password(pwd)
				u.save()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data
