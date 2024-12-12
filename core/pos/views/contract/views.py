import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.pos.forms import Contract, ContractForm
from core.pos.models import Employee
from core.security.mixins import GroupPermissionMixin


class ContractListView(GroupPermissionMixin, TemplateView):
    template_name = 'contract/list.html'
    permission_required = 'view_contract'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Contract.objects.all():
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Contratos'
        context['create_url'] = reverse_lazy('contract_create')
        return context


class ContractCreateView(GroupPermissionMixin, CreateView):
    model = Contract
    template_name = 'contract/create.html'
    form_class = ContractForm
    success_url = reverse_lazy('contract_list')
    permission_required = 'add_contract'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        employee_id = list(Contract.objects.exclude(active=False).values_list('employee_id', flat=True).distinct())
        form.fields['employee'].queryset = Employee.objects.filter().exclude(id__in=employee_id)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Contrato'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ContractUpdateView(GroupPermissionMixin, UpdateView):
    model = Contract
    template_name = 'contract/create.html'
    form_class = ContractForm
    success_url = reverse_lazy('contract_list')
    permission_required = 'change_contract'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['employee'].disabled = True
        return form

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Contrato'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ContractDeleteView(GroupPermissionMixin, DeleteView):
    model = Contract
    template_name = 'delete.html'
    success_url = reverse_lazy('contract_list')
    permission_required = 'delete_contract'

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
