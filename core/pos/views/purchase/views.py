import json
import random
import string

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView

from core.pos.forms import PurchaseForm, Purchase, Inventory, Resource, Provider, ProviderForm
from core.reports.forms import ReportForm
from core.security.mixins import GroupPermissionMixin


class PurchaseListView(GroupPermissionMixin, FormView):
    template_name = 'purchase/list.html'
    form_class = ReportForm
    permission_required = 'view_purchase'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                filters = Q()
                if len(start_date) and len(end_date):
                    filters &= Q(date_joined__range=[start_date, end_date])
                for i in Purchase.objects.filter(filters):
                    data.append(i.as_dict())
            elif action == 'search_detail':
                data = []
                for i in Inventory.objects.filter(purchase_id=request.POST['id']):
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['create_url'] = reverse_lazy('purchase_create')
        return context


class PurchaseCreateView(GroupPermissionMixin, CreateView):
    model = Purchase
    template_name = 'purchase/create.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchase_list')
    permission_required = 'add_purchase'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['disabled_fields'] = ['subtotal', 'tax', 'total_tax', 'total_amount']
        return kwargs

    def generate_random_series(self):
        letters_numbers = string.ascii_lowercase + string.digits
        return ''.join(random.choices(letters_numbers, k=10)).upper()

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    detail = json.loads(request.POST['detail'])
                    purchase = Purchase()
                    purchase.number = request.POST['number']
                    purchase.provider_id = int(request.POST['provider'])
                    purchase.date_joined = request.POST['date_joined']
                    purchase.tax = float(detail['tax']) / 100
                    purchase.save()
                    for i in detail['resources']:
                        resource = Resource.objects.get(id=i['id'])
                        if not resource.is_equipment and len(i['series']) == 0:
                            Inventory.objects.create(purchase_id=purchase.id, resource_id=resource.id, price=resource.price, quantity=i['quantity'])
                        else:
                            for equipment in i['series']:
                                Inventory.objects.create(purchase_id=purchase.id, resource_id=resource.id, price=resource.price, quantity=1, serie=equipment['serie'], guarantee=equipment['guarantee'])
                    purchase.calculate_detail()
                    purchase.calculate_invoice()
            elif action == 'generate_random_serie':
                serie = self.generate_random_series()
                while Inventory.objects.filter(serie=serie, active=True).exists():
                    serie = self.generate_random_series()
                data['serie'] = serie
            elif action == 'search_resource':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                filters = Q()
                if len(term):
                    filters &= Q(Q(name__icontains=term) | Q(code__icontains=term))
                queryset = Resource.objects.filter(filters).exclude(id__in=ids).order_by('name')
                if filters.children and len(term):
                    queryset = queryset[0:10]
                for i in queryset:
                    item = i.as_dict()
                    item['series'] = []
                    data.append(item)
            elif action == 'search_provider':
                data = []
                term = request.POST['term']
                for i in Provider.objects.filter(Q(name__icontains=term) | Q(ruc__icontains=term)).order_by('name')[0:10]:
                    data.append(i.as_dict())
            elif action == 'validate_provider':
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
            elif action == 'validate_purchase':
                data['valid'] = not Purchase.objects.filter(number=request.POST['number']).exists()
            elif action == 'validate_serie':
                serie = request.POST['serie']
                series = json.loads(request.POST['series'])
                data = {'valid': serie not in series and not Inventory.objects.filter(serie=serie).exclude(serie__in=series).exists()}
            elif action == 'create_provider':
                form = ProviderForm(request.POST)
                data = form.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Compra'
        context['frmProvider'] = ProviderForm()
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class PurchaseDeleteView(GroupPermissionMixin, DeleteView):
    model = Purchase
    template_name = 'delete.html'
    success_url = reverse_lazy('purchase_list')
    permission_required = 'delete_purchase'

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
