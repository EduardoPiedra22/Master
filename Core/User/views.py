from datetime import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView
from django.shortcuts import render

from Core.mixins import *
from Core.User.forms import *
from Core.User.models import User

# Create your views here.

class UserListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
	model = User
	permission_required = 'view_user'
	template_name = "usuario/Usuarios_lista.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'searchdata':
				data = []
				position = 1
				for i in User.objects.all():
					item = i.toJSON()
					item['position'] = position
					data.append(item)

					position +=1
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Lista de Usuarios'
		context['url'] = 'Usuarios'
		context['title_body'] = 'Listado de Usuarios'
		context['date_now'] = datetime.now()
		context['create_url'] = reverse_lazy('user:User_crear')
		context['list_url'] = reverse_lazy('user:User_lista')

		return context



class UserCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
	model = User
	form_class = UserForm
	template_name = 'usuario/Usuarios_form.html'
	permission_required = 'add_user'
	success_url = reverse_lazy('user:User_lista')

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'add':
				form = self.get_form()
				data = form.save()
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Formulario de Usuarios'
		context['url'] = 'Usuarios'
		context['title_body'] = 'Formulario de Usuarios'
		context['list_url'] = reverse_lazy('user:User_lista')
		context['action'] = 'add'
		return context

	def update(self):
		pass


class UserUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
	model = User
	form_class = UserForm
	template_name = 'usuario/Usuarios_form.html'
	permission_required = 'change_user'
	success_url = reverse_lazy('user:User_lista')

	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'edit':
				form = self.get_form()
				data = form.save()
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Editar de Usuarios'
		context['url'] = 'Usuarios'
		context['title_body'] = 'Editar Usuarios'
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		return context


class UserDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
	model = User
	template_name = 'usuario/Usuarios_delete.html'
	permission_required = 'delete_user'
	success_url = reverse_lazy('user:User_lista')

	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().dispatch(request, *args, **kwargs)


	def post(self, request, *args, **kwargs):
		data = {}
		try:
			self.object.delete()
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Eliminar de Usuarios'
		context['url'] = 'Usuarios'
		context['title_body'] = 'Eliminar un Usuario'
		context['list_url'] = reverse_lazy('user:User_lista')
		return context


class UserChangeGropus(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('app:dashboard'))


class UserProfileView(LoginRequiredMixin, UpdateView):
	model = User
	form_class = UserProfileForm
	template_name = 'usuario/Profile.html'
	success_url = reverse_lazy('app:dashboard')

	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		return self.request.user


	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'edit':
				form = self.get_form()
				data = form.save()
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Editar Perfil'
		context['url'] = 'Perfil'
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		return context



class UserChangePasswordView(LoginRequiredMixin, FormView):
	model = User
	form_class = PasswordChangeForm
	template_name = 'usuario/Change_password.html'
	success_url = reverse_lazy('login:login')

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def get_form(self, form_class=None):
		form = PasswordChangeForm(user=self.request.user)
		form.fields['old_password'].widget.attrs['class'] = 'form-control'
		form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
		form.fields['new_password1'].widget.attrs['class'] = 'form-control'
		form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
		form.fields['new_password2'].widget.attrs['class'] = 'form-control'
		form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
		return form


	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'edit':
				form = PasswordChangeForm(user=request.user, data=request.POST)
				if form.is_valid():
					form.save()
					update_session_auth_hash(request, form.user)
				else:
					data['error'] = form.errors
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Editar Password'
		context['url'] = 'Password'
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		return context

