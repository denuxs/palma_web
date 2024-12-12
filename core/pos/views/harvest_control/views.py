import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, DeleteView

from core.pos.forms import HarvestControl, HarvestControlForm, TapeAssignment, Tape
from core.pos.models import HarvestControlDetail, Production
from core.reports.forms import ReportForm
from core.security.mixins import GroupPermissionMixin


class HarvestControlListView(GroupPermissionMixin, FormView):
    template_name = 'harvest_control/list.html'
    form_class = ReportForm
    permission_required = 'view_harvest_control'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                filters = Q()
                if len(start_date) and len(end_date):
                    filters &= Q(date_joined__range=[start_date, end_date])
                for i in HarvestControl.objects.filter(filters):
                    data.append(i.as_dict())
            elif action == 'search_harvest_control_detail':
                data = []
                for i in HarvestControlDetail.objects.filter(harvest_control_id=request.POST['id']):
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Control de Cosecha'
        context['create_url'] = reverse_lazy('harvest_control_create')
        return context


class HarvestControlCreateView(GroupPermissionMixin, CreateView):
    model = HarvestControl
    template_name = 'harvest_control/create.html'
    form_class = HarvestControlForm
    success_url = reverse_lazy('harvest_control_list')
    permission_required = 'add_harvest_control'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    harvest_control = HarvestControl.objects.update_or_create(
                        production_id=request.POST['production'],
                        defaults={
                            'date_joined': request.POST['date_joined'],
                            'observations': request.POST['observations']
                        }
                    )[0]
                    harvest_control.harvestcontroldetail_set.all().delete()
                    for detail in json.loads(request.POST['detail']):
                        tape_assignment = TapeAssignment.objects.get(id=detail['id'])
                        HarvestControlDetail.objects.create(harvest_control_id=harvest_control.id, plant_type_id=tape_assignment.production_plant.plant.plant_type_id, tape_assignment_id=tape_assignment.id, quantity=detail['quantity'], boxes=detail['boxes'])
                    harvest_control.calculate_totals()
                    harvest_control.production.active = False
                    harvest_control.production.save()
            elif action == 'search_tape_assignment':
                data = {'rows': [], 'production': dict(), 'notification': ''}
                production_id = request.POST['id']
                if len(production_id):
                    production = Production.objects.get(id=production_id)
                    data['production'] = production.as_dict()
                    if not production.active:
                        data['notification'] = 'La producción está inactiva, por lo que ya no es posible cosechar'
                    else:
                        tape_last = Tape.objects.filter().order_by('-week').first()
                        queryset = TapeAssignment.objects.filter(production_plant__production_id=production.id, tape_id=tape_last.id).exclude(production_plant__production__active=False)
                        if not queryset.exists():
                            data['notification'] = 'La producción aún no tiene la última cinta registrada, por lo tanto, no es posible cosechar'
                        for i in queryset:
                            item = i.as_dict()
                            item['tape'] = tape_last.as_dict()
                            item['latest_fruit_control_quantity'] = i.latest_fruit_control_quantity
                            item['quantity'] = i.latest_fruit_control_quantity
                            item['boxes'] = 0
                            data['rows'].append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Control de Cosecha'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class HarvestControlDeleteView(GroupPermissionMixin, DeleteView):
    model = HarvestControl
    template_name = 'delete.html'
    success_url = reverse_lazy('harvest_control_list')
    permission_required = 'delete_harvest_control'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
