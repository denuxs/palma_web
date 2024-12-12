import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, DeleteView

from core.pos.forms import ActivityControl, ActivityControlForm, TapeAssignment, Tape, Activity
from core.reports.forms import ReportForm
from core.security.mixins import GroupPermissionMixin


class ActivityControlListView(GroupPermissionMixin, FormView):
    template_name = 'activity_control/list.html'
    form_class = ReportForm
    permission_required = 'view_activity_control'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                filters = Q()
                production = request.POST['production']
                tape = request.POST['tape']
                activity = request.POST['activity']
                if len(production):
                    filters &= Q(tape_assignment__production_plant__production_id=production)
                if len(tape):
                    filters &= Q(tape_assignment__tape_id=tape)
                if len(activity):
                    filters &= Q(activity__id=activity)
                for i in ActivityControl.objects.filter(filters):
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Control de Actividades Agronómicas'
        context['create_url'] = reverse_lazy('activity_control_create')
        return context


class ActivityControlCreateView(GroupPermissionMixin, CreateView):
    model = ActivityControl
    template_name = 'activity_control/create.html'
    form_class = ActivityControlForm
    success_url = reverse_lazy('activity_control_list')
    permission_required = 'add_activity_control'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    date_joined = request.POST['date_joined']
                    for detail in json.loads(request.POST['detail']):
                        ActivityControl.objects.create(tape_assignment_id=detail['id'], activity_id=int(detail['activity']['id']), date_joined=date_joined, observations=detail['observations'])
            elif action == 'search_tape_assignment':
                data = []
                production_id = request.POST['id']
                if len(production_id):
                    queryset = TapeAssignment.objects.filter(production_plant__production_id=production_id)
                    tapes = list(queryset.order_by('-tape__week').values_list('tape_id', flat=True).distinct())
                    if len(tapes):
                        tape = Tape.objects.get(id=tapes[0])
                        activity = Activity.objects.first().as_dict()
                        for i in queryset.filter(tape_id=tape.id):
                            item = i.as_dict()
                            item['observations'] = ''
                            item['selected'] = 0
                            item['tape'] = tape.as_dict()
                            item['activity'] = activity
                            data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_activities(self):
        data = []
        for i in Activity.objects.all():
            item = i.as_dict().copy()
            item['data'] = i.as_dict()
            data.append(item)
        return json.dumps(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Control de Actividad Agronómica'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['activities'] = self.get_activities()
        return context
    

class ActivityControlDeleteView(GroupPermissionMixin, DeleteView):
    model = ActivityControl
    template_name = 'delete.html'
    success_url = reverse_lazy('activity_control_list')
    permission_required = 'delete_activity_control'

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
