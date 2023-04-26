
from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView, View
from Core.reportes.forms import ReportsForm
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


from django.template.loader import get_template

from Core.solicitud.models import *
from Core.solicitante.models import *

class ReportesView(TemplateView):
	template_name='report/reportes.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'search_report':
				data = []
				start_date = request.POST.get('start_date', '')
				end_date = request.POST.get('end_date', '')
				search = Solicitudes.objects.all()
				if len(start_date) and len(end_date):
					search = search.filter(fecha_registro__range=[start_date, end_date])
				for s in search:
					data.append([
						s.id,
						s.categoria.nombre,
						s.id_solicitante.get_full_name(),
						s.estatus,
						s.fecha_registro.strftime('%Y-%m-%d'),
						])
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)



	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context ['title'] = 'Reportes de solicitudes'
		context['url'] = 'Reportes'
		context['title_body'] = 'Reportes de Solicitudes'
		context['enhead_body'] = 'Secretaria de Desarrollo Humano y Comunal'
		context['date_now'] = datetime.now()

		context['form'] = ReportsForm()
		return context


class ReportesBaseMisionesView(TemplateView):
	template_name='report/reportes_misiones.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'search_report':
				data = []
				start_date = request.POST.get('start_date', '')
				end_date = request.POST.get('end_date', '')
				search = BaseGrandesMisiones.objects.all()
				if len(start_date) and len(end_date):
					search = search.filter(fecha_registro__range=[start_date, end_date])
				for s in search:
					data.append([
						s.id,
						s.nombre,
						s.responsable.get_full_name(),
						s.municipio,
						s.nombre_p,
						s.nombre_c,
						])
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)



	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context ['title'] = 'Reportes de Misiones y Grandes Misiones'
		context['url'] = 'Reportes de Misiones y Grandes Misiones'
		context['title_body'] = 'Reportes de Misiones y Grandes Misiones'
		context['date_now'] = datetime.now()
		context['form'] = ReportsForm()
		return context

"""
       class ReportesPdfView(View):
           def get(self, request, *args, **kwargs):
               try:
                   template = get_template('ingresos_prod/guia_ingresoPDF.html')
                   context = {
                       'ingreso': Solicitudes.objects.get(pk=self.kwargs['pk']),
                       'comp': {'name': 'PROY-UNIVERSIDAD S.A.', 'ruc': '13041273', 'address': 'Guanare Estado Portuguesa, Venezuela'},
                       'icon': '{}{}'.format(settings.MEDIA_URL, 'imagportadalogin/klipartzcom.png')
                   }
                  
                   html = template.render(context)
                   css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0-dist/css/bootstrap.min.css')
                   pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
                   return HttpResponse(pdf, content_type='application/pdf')
               except:
                   pass
               return HttpResponseRedirect(reverse_lazy('app:dashboard'))
"""


