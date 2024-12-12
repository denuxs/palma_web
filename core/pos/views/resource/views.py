import json

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from core.pos.forms import ResourceForm, Resource
from core.pos.models import Inventory
from core.security.mixins import GroupPermissionMixin


class ResourceListView(GroupPermissionMixin, TemplateView):
    template_name = 'resource/list.html'
    permission_required = 'view_resource'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Resource.objects.filter():
                    data.append(i.as_dict())
            elif action == 'search_inventory':
                data = []
                for i in Inventory.objects.filter(resource_id=request.POST['id'], saldo__gt=0, active=True):
                    item = i.as_dict()
                    item['purchase'] = i.purchase.as_dict()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Insumos y Equipos'
        context['create_url'] = reverse_lazy('resource_create')
        return context


class ResourceCreateView(GroupPermissionMixin, CreateView):
    model = Resource
    template_name = 'resource/create.html'
    form_class = ResourceForm
    success_url = reverse_lazy('resource_list')
    permission_required = 'add_resource'

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
                data['valid'] = not Resource.objects.filter(filters).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Recurso'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ResourceUpdateView(GroupPermissionMixin, UpdateView):
    model = Resource
    template_name = 'resource/create.html'
    form_class = ResourceForm
    success_url = reverse_lazy('resource_list')
    permission_required = 'change_resource'

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
                data['valid'] = not Resource.objects.filter(filters).exclude(id=self.object.id).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Recurso'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ResourceDeleteView(GroupPermissionMixin, DeleteView):
    model = Resource
    template_name = 'delete.html'
    success_url = reverse_lazy('resource_list')
    permission_required = 'delete_resource'

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
