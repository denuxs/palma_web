import calendar
import json
import locale
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import TemplateView

from core.pos.models import Client, Provider, Employee, Activity, PlantType, Invoice, Production
from core.security.models import Dashboard


class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        dashboard = Dashboard.objects.first()
        if dashboard and dashboard.layout == 1:
            return 'vtc_dashboard.html'
        return 'hzt_dashboard.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        errors = {}
        action = request.POST['action']
        try:
            if action == 'get_graph_stock_plants':
                data = []
                for i in PlantType.objects.filter():
                    stock = i.stock
                    if stock:
                        data.append({'name': i.name, 'y': stock})
            elif action == 'get_graph_invoice_year':
                data = []
                year = datetime.now().year
                # locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                for month in range(1, 13):
                    result = Invoice.objects.filter(date_joined__month=month, date_joined__year=year).aggregate(result=Coalesce(Sum('total_amount'), 0.00, output_field=FloatField()))['result']
                    data.append([calendar.month_name[month].title(), result])
            else:
                errors['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            print(e)
            errors['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['clients'] = Client.objects.all().count()
        context['employees'] = Employee.objects.all().count()
        context['providers'] = Provider.objects.all().count()
        context['activities'] = Activity.objects.all().count()
        context['productions'] = Production.objects.all().count()
        context['plant_types'] = PlantType.objects.all().count()
        context['invoices'] = Invoice.objects.all().order_by('-id')[0:10]
        return context
