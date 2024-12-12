import json

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.pos.forms import Lot, LotForm
from core.security.mixins import GroupPermissionMixin


class LotListView(GroupPermissionMixin, TemplateView):
    template_name = 'lot/list.html'
    permission_required = 'view_lot'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Lot.objects.all():
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Lotes'
        context['create_url'] = reverse_lazy('lot_create')
        return context


class LotCreateView(GroupPermissionMixin, CreateView):
    model = Lot
    template_name = 'lot/create.html'
    form_class = LotForm
    success_url = reverse_lazy('lot_list')
    permission_required = 'add_lot'

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
                data['valid'] = not Lot.objects.filter(filters).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Lote'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class LotUpdateView(GroupPermissionMixin, UpdateView):
    model = Lot
    template_name = 'lot/create.html'
    form_class = LotForm
    success_url = reverse_lazy('lot_list')
    permission_required = 'change_lot'

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
                data['valid'] = not Lot.objects.filter(filters).exclude(id=self.object.id).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Lote'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class LotDeleteView(GroupPermissionMixin, DeleteView):
    model = Lot
    template_name = 'delete.html'
    success_url = reverse_lazy('lot_list')
    permission_required = 'delete_lot'

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
