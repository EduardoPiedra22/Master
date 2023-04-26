import smtplib
import uuid

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import *
import Config.settings as settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from Config.wsgi import*
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string

from Core.User.models import *

from .forms import *
# Create your views here.


class LoginFormView(FormView):
	form_class = AuthenticationForm
	template_name = 'login/Login.html'
	success_url = reverse_lazy('app:dashboard')

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(self.success_url)
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		login(self.request, form.get_user())
		return HttpResponseRedirect(self.success_url)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Iniciar Sesion'
		return context



class ResetPassWordView(FormView):
	form_class = ResetPassWordForm
	template_name = 'login/resetpwd.html'
	success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)


	def send_email_reset_pwd(self, User):
		data = {}
		try:
			URL= settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']


			User.token = uuid.uuid4()
			User.save()

			mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
			mailServer.starttls()
			mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        	# Construimos el mensaje simple
        	# Plantilla optenida de beefree.io

			email_to = User.email
			mensaje = MIMEMultipart()
			mensaje['From'] = settings.EMAIL_HOST_USER
			mensaje['To'] = email_to
			mensaje['Subject'] = "reseteo de contraseña"

			content = render_to_string('login/send_email.html', {
				'user': User, 
				'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(User.token)),
				'link_home': 'http://{}'.format(URL)

        	})
			mensaje.attach(MIMEText(content, 'html'))

			mailServer.sendmail(settings.EMAIL_HOST_USER,
		                    email_to,
		                    mensaje.as_string())

		except Exception as e:
			data['error'] = str(e)
		
		return data

	

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			form = ResetPassWordForm(request.POST)  # es lo mismo que utilizar == self.get_form
			print(request.POST)
			if form.is_valid():
			    user = form.get_user()
			    data = self.send_email_reset_pwd(user)
			else:
				data['error'] = form.errors
		except Exception as e:
		    data['error'] = str(e)
		return JsonResponse(data, safe=False)



	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Reseteo de Contraseña'
		return context



class ChangePassWordView(FormView):
	form_class = ChangedPassWordForm
	template_name = 'login/Changepwd.html'
	success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)


	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)


	def get(self, request, *args, **kwargs):
		token = self.kwargs['token']
		if User.objects.filter(token=token).exists():
			return super().get(request, *args, **kwargs)
		return HttpResponseRedirect(settings.LOGIN_URL)


	def post(self, request, *args, **kwargs):
		data = {}
		try:
			form = ChangedPassWordForm(request.POST)
			if form.is_valid():
				user = User.objects.get(token=self.kwargs['token'])
				user.set_password(request.POST['password'])
				user.token = uuid.uuid4()
				user.save()
			else:
				data['error'] = form.errors

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Recuperar Contraseña'
		context['login_url'] = settings.LOGIN_URL
		return context