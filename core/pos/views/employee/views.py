import json

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from core.pos.forms import EmployeeForm, Employee
from core.security.mixins import GroupPermissionMixin


class EmployeeListView(GroupPermissionMixin, TemplateView):
    template_name = 'employee/list.html'
    permission_required = 'view_employee'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Employee.objects.filter():
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Empleados'
        context['create_url'] = reverse_lazy('employee_create')
        return context


class EmployeeCreateView(GroupPermissionMixin, CreateView):
    model = Employee
    template_name = 'employee/create.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    permission_required = 'add_employee'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                field = request.POST['field']
                filters = Q()
                if field == 'dni':
                    filters &= Q(dni__iexact=request.POST['dni'])
                elif field == 'mobile':
                    filters &= Q(mobile__iexact=request.POST['mobile'])
                elif field == 'email':
                    filters &= Q(email__iexact=request.POST['email'])
                data['valid'] = not Employee.objects.filter(filters).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de un Empleado'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class EmployeeUpdateView(GroupPermissionMixin, UpdateView):
    model = Employee
    template_name = 'employee/create.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    permission_required = 'change_employee'

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
                if field == 'dni':
                    filters &= Q(dni__iexact=request.POST['dni'])
                elif field == 'mobile':
                    filters &= Q(mobile__iexact=request.POST['mobile'])
                elif field == 'email':
                    filters &= Q(email__iexact=request.POST['email'])
                data['valid'] = not Employee.objects.filter(filters).exclude(id=self.object.id).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de un Empleado'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class EmployeeDeleteView(GroupPermissionMixin, DeleteView):
    model = Employee
    template_name = 'delete.html'
    success_url = reverse_lazy('employee_list')
    permission_required = 'delete_employee'

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
