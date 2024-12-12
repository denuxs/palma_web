import json

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.pos.forms import Tape, TapeForm
from core.security.mixins import GroupPermissionMixin


class TapeListView(GroupPermissionMixin, TemplateView):
    template_name = 'tape/list.html'
    permission_required = 'view_tape'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Tape.objects.filter().order_by('week'):
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cintas'
        context['create_url'] = reverse_lazy('tape_create')
        return context


class TapeCreateView(GroupPermissionMixin, CreateView):
    model = Tape
    template_name = 'tape/create.html'
    form_class = TapeForm
    success_url = reverse_lazy('tape_list')
    permission_required = 'add_tape'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                field = request.POST['field']
                filters = Q()
                if field == 'week':
                    filters &= Q(week__iexact=request.POST['week'])
                data['valid'] = not Tape.objects.filter(filters).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Cinta'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TapeUpdateView(GroupPermissionMixin, UpdateView):
    model = Tape
    template_name = 'tape/create.html'
    form_class = TapeForm
    success_url = reverse_lazy('tape_list')
    permission_required = 'change_tape'

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
                if field == 'week':
                    filters &= Q(week__iexact=request.POST['week'])
                data['valid'] = not Tape.objects.filter(filters).exclude(id=self.object.id).exists() if filters.children else True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Edición de una Cinta'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TapeDeleteView(GroupPermissionMixin, DeleteView):
    model = Tape
    template_name = 'delete.html'
    success_url = reverse_lazy('tape_list')
    permission_required = 'delete_tape'

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
