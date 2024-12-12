import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, DeleteView

from core.pos.forms import TapedFruitControl, TapedFruitControlForm, TapeAssignment, Tape
from core.reports.forms import ReportForm
from core.security.mixins import GroupPermissionMixin


class TapedFruitControlListView(GroupPermissionMixin, FormView):
    template_name = 'taped_fruit_control/list.html'
    form_class = ReportForm
    permission_required = 'view_taped_fruit_control'

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
                    filters &= Q(tape_assignment__production_plant__production_id=production)
                if len(tape):
                    filters &= Q(tape_assignment__tape_id=tape)
                for i in TapedFruitControl.objects.filter(filters):
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Control de Fruta Encintada'
        context['create_url'] = reverse_lazy('taped_fruit_control_create')
        return context


class TapedFruitControlCreateView(GroupPermissionMixin, CreateView):
    model = TapedFruitControl
    template_name = 'taped_fruit_control/create.html'
    form_class = TapedFruitControlForm
    success_url = reverse_lazy('taped_fruit_control_list')
    permission_required = 'add_taped_fruit_control'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    date_joined = request.POST['date_joined']
                    for detail in json.loads(request.POST['detail']):
                        TapedFruitControl.objects.create(tape_assignment_id=detail['id'], date_joined=date_joined, quantity=detail['quantity'], observations=detail['observations'])
            elif action == 'search_tape_assignment':
                data = []
                production_id = request.POST['id']
                if len(production_id):
                    queryset = TapeAssignment.objects.filter(production_plant__production_id=production_id)
                    tapes = list(queryset.order_by('-tape__week').values_list('tape_id', flat=True).distinct())
                    if len(tapes):
                        tape = Tape.objects.get(id=tapes[0])
                        for i in queryset.filter(tape_id=tape.id):
                            item = i.as_dict()
                            item['observations'] = ''
                            item['selected'] = 0
                            item['tape'] = tape.as_dict()
                            item['quantity'] = i.latest_fruit_control_quantity
                            data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Control de Fruta Encintada'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TapedFruitControlDeleteView(GroupPermissionMixin, DeleteView):
    model = TapedFruitControl
    template_name = 'delete.html'
    success_url = reverse_lazy('taped_fruit_control_list')
    permission_required = 'delete_taped_fruit_control'

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
