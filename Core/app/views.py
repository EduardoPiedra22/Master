from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import *

from Core.solicitud.models import Solicitudes

from random import randint
# Create your views here.

class Index(TemplateView):
    template_name = "app/body.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)


    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Solicitudes.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(
                    r=Coalesce(Sum('total'), 0)).get('r')
                data.append(int(total))
        except:
            pass
        return data


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administrador'
        context['title_body'] = 'Dashboard'
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        return context


