import json

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.pos.forms import PlantType, PlantTypeForm, HarvestControlDetail
from core.security.mixins import GroupPermissionMixin


class PlantTypeListView(GroupPermissionMixin, TemplateView):
    template_name = 'plant_type/list.html'
    permission_required = 'view_plant_type'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in PlantType.objects.all():
                    data.append(i.as_dict())
            elif action == 'search_inventory':
                data = []
                for i in HarvestControlDetail.objects.filter(plant_type_id=request.POST['id'], saldo__gt=0, active=True):
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Plantas'
        context['create_url'] = reverse_lazy('plant_type_create')
        return context


class PlantTypeCreateView(GroupPermissionMixin, CreateView):
    model = PlantType
    template_name = 'plant_type/create.html'
    form_class = PlantTypeForm
    success_url = reverse_lazy('plant_type_list')
    permission_required = 'add_plant_type'

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
                elif field == 'name':
                    filters &= Q(name__iexact=request.POST['name'])
                data['valid'] = not PlantType.objects.filter(filters).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Planta'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class PlantTypeUpdateView(GroupPermissionMixin, UpdateView):
    model = PlantType
    template_name = 'plant_type/create.html'
    form_class = PlantTypeForm
    success_url = reverse_lazy('plant_type_list')
    permission_required = 'change_plant_type'

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
                elif field == 'name':
                    filters &= Q(name__iexact=request.POST['name'])
                data['valid'] = not PlantType.objects.filter(filters).exclude(id=self.object.id).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de una Planta'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class PlantTypeDeleteView(GroupPermissionMixin, DeleteView):
    model = PlantType
    template_name = 'delete.html'
    success_url = reverse_lazy('plant_type_list')
    permission_required = 'delete_plant_type'

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
