import json

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.pos.forms import TypeExpense, TypeExpenseForm
from core.security.mixins import GroupPermissionMixin


class TypeExpenseListView(GroupPermissionMixin, TemplateView):
    template_name = 'type_expense/list.html'
    permission_required = 'view_type_expense'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in TypeExpense.objects.all():
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipos de Gastos'
        context['create_url'] = reverse_lazy('type_expense_create')
        return context


class TypeExpenseCreateView(GroupPermissionMixin, CreateView):
    model = TypeExpense
    template_name = 'type_expense/create.html'
    form_class = TypeExpenseForm
    success_url = reverse_lazy('type_expense_list')
    permission_required = 'add_type_expense'

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
                data['valid'] = not TypeExpense.objects.filter(filters).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Tipo de Gasto'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TypeExpenseUpdateView(GroupPermissionMixin, UpdateView):
    model = TypeExpense
    template_name = 'type_expense/create.html'
    form_class = TypeExpenseForm
    success_url = reverse_lazy('type_expense_list')
    permission_required = 'change_type_expense'

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
                data['valid'] = not TypeExpense.objects.filter(filters).exclude(id=self.object.id).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Tipo de Gasto'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TypeExpenseDeleteView(GroupPermissionMixin, DeleteView):
    model = TypeExpense
    template_name = 'delete.html'
    success_url = reverse_lazy('type_expense_list')
    permission_required = 'delete_type_expense'

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
