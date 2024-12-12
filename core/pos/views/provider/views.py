import json

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.pos.forms import Provider, ProviderForm
from core.security.mixins import GroupPermissionMixin


class ProviderListView(GroupPermissionMixin, TemplateView):
    template_name = 'provider/list.html'
    permission_required = 'view_provider'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Provider.objects.all():
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proveedores'
        context['create_url'] = reverse_lazy('provider_create')
        return context


class ProviderCreateView(GroupPermissionMixin, CreateView):
    model = Provider
    template_name = 'provider/create.html'
    form_class = ProviderForm
    success_url = reverse_lazy('provider_list')
    permission_required = 'add_provider'

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
                elif field == 'ruc':
                    filters &= Q(ruc__iexact=request.POST['ruc'])
                elif field == 'mobile':
                    filters &= Q(mobile__iexact=request.POST['mobile'])
                elif field == 'email':
                    filters &= Q(email__iexact=request.POST['email'])
                data['valid'] = not Provider.objects.filter(filters).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Proveedor'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ProviderUpdateView(GroupPermissionMixin, UpdateView):
    model = Provider
    template_name = 'provider/create.html'
    form_class = ProviderForm
    success_url = reverse_lazy('provider_list')
    permission_required = 'change_provider'

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
                elif field == 'ruc':
                    filters &= Q(ruc__iexact=request.POST['ruc'])
                elif field == 'mobile':
                    filters &= Q(mobile__iexact=request.POST['mobile'])
                elif field == 'email':
                    filters &= Q(email__iexact=request.POST['email'])
                data['valid'] = not Provider.objects.filter(filters).exclude(id=self.object.id).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Proveedor'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ProviderDeleteView(GroupPermissionMixin, DeleteView):
    model = Provider
    template_name = 'delete.html'
    success_url = reverse_lazy('provider_list')
    permission_required = 'delete_provider'

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
