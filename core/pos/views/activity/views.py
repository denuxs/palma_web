import json

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.pos.forms import Activity, ActivityForm
from core.security.mixins import GroupPermissionMixin


class ActivityListView(GroupPermissionMixin, TemplateView):
    template_name = 'activity/list.html'
    permission_required = 'view_activity'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Activity.objects.all():
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Actividades de Cosecha'
        context['create_url'] = reverse_lazy('activity_create')
        return context


class ActivityCreateView(GroupPermissionMixin, CreateView):
    model = Activity
    template_name = 'activity/create.html'
    form_class = ActivityForm
    success_url = reverse_lazy('activity_list')
    permission_required = 'add_activity'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                field = request.POST['field']
                filters = Q()
                if field == 'name':
                    filters &= Q(name__iexact=request.POST['name'])
                data['valid'] = not Activity.objects.filter(filters).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Actividad'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ActivityUpdateView(GroupPermissionMixin, UpdateView):
    model = Activity
    template_name = 'activity/create.html'
    form_class = ActivityForm
    success_url = reverse_lazy('activity_list')
    permission_required = 'change_activity'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                field = request.POST['field']
                filters = Q()
                if field == 'name':
                    filters &= Q(name__iexact=request.POST['name'])
                data['valid'] = not Activity.objects.filter(filters).exclude(id=self.object.id).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de una Actividad'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ActivityDeleteView(GroupPermissionMixin, DeleteView):
    model = Activity
    template_name = 'delete.html'
    success_url = reverse_lazy('activity_list')
    permission_required = 'delete_activity'

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
