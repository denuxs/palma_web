import json

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.pos.forms import Plant, PlantForm
from core.security.mixins import GroupPermissionMixin


class PlantListView(GroupPermissionMixin, TemplateView):
    template_name = 'plant/list.html'
    permission_required = 'view_plant'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Plant.objects.all():
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Registros de Plantas'
        context['create_url'] = reverse_lazy('plant_create')
        return context


class PlantCreateView(GroupPermissionMixin, CreateView):
    model = Plant
    template_name = 'plant/create.html'
    form_class = PlantForm
    success_url = reverse_lazy('plant_list')
    permission_required = 'add_plant'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                field = request.POST['field']
                filters = Q()
                if field == 'code':
                    filters &= Q(code__iexact=request.POST['code'])
                data['valid'] = not Plant.objects.filter(filters).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Registro de Planta'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class PlantUpdateView(GroupPermissionMixin, UpdateView):
    model = Plant
    template_name = 'plant/create.html'
    form_class = PlantForm
    success_url = reverse_lazy('plant_list')
    permission_required = 'change_plant'

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
                if field == 'code':
                    filters &= Q(code__iexact=request.POST['code'])
                data['valid'] = not Plant.objects.filter(filters).exclude(id=self.object.id).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Registro de Planta'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class PlantDeleteView(GroupPermissionMixin, DeleteView):
    model = Plant
    template_name = 'delete.html'
    success_url = reverse_lazy('plant_list')
    permission_required = 'delete_plant'

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
