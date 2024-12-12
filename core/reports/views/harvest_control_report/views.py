import json

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import FormView

from core.pos.models import HarvestControl, HarvestControlDetail
from core.reports.forms import ReportForm
from core.security.mixins import GroupModuleMixin


class HarvestControlReportView(GroupModuleMixin, FormView):
    template_name = 'harvest_control_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                filters = Q()
                if len(start_date) and len(end_date):
                    filters &= Q(date_joined__range=[start_date, end_date])
                for i in HarvestControl.objects.filter(filters):
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Cosechas'
        return context


class HarvestControlDetailReportView(GroupModuleMixin, FormView):
    template_name = 'harvest_control_detail_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                filters = Q()
                if len(start_date) and len(end_date):
                    filters &= Q(harvest_control__date_joined__range=[start_date, end_date])
                for i in HarvestControlDetail.objects.filter(filters):
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Inventario de Cosecha'
        return context
