import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, DeleteView

from core.pos.forms import TapeAssignment, TapeAssignmentForm, ProductionPlant
from core.reports.forms import ReportForm
from core.security.mixins import GroupPermissionMixin


class TapeAssignmentListView(GroupPermissionMixin, FormView):
    template_name = 'tape_assignment/list.html'
    form_class = ReportForm
    permission_required = 'view_tape_assignment'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                filters = Q()
                production = request.POST['production']
                tape = request.POST['tape']
                if len(production):
                    filters &= Q(production_plant__production__id=production)
                if len(tape):
                    filters &= Q(tape_id=tape)
                for i in TapeAssignment.objects.filter(filters):
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Asignaciones de cintas por semana'
        context['create_url'] = reverse_lazy('tape_assignment_create')
        return context


class TapeAssignmentCreateView(GroupPermissionMixin, CreateView):
    model = TapeAssignment
    template_name = 'tape_assignment/create.html'
    form_class = TapeAssignmentForm
    success_url = reverse_lazy('tape_assignment_list')
    permission_required = 'add_tape_assignment'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    date_joined = request.POST['date_joined']
                    for detail in json.loads(request.POST['detail']):
                        TapeAssignment.objects.create(production_plant_id=detail['id'], tape_id=int(detail['next']['id']), date_joined=date_joined, observations=detail['observations'])
            elif action == 'search_plant':
                data = []
                production_id = request.POST['id']
                if len(production_id):
                    for i in ProductionPlant.objects.filter(production_id=production_id):
                        item = i.as_dict()
                        item['observations'] = ''
                        item['selected'] = 0
                        item.update(i.get_tapes())
                        data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Asignación de cintas por semana'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TapeAssignmentDeleteView(GroupPermissionMixin, DeleteView):
    model = TapeAssignment
    template_name = 'delete.html'
    success_url = reverse_lazy('tape_assignment_list')
    permission_required = 'delete_tape_assignment'

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
