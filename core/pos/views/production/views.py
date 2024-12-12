import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, DeleteView

from core.pos.forms import Production, ProductionForm, Contract, Resource, Inventory, Plant, ProductionPlant, ProductionContract, ProductionResource, PLANT_STATUS
from core.reports.forms import ReportForm
from core.security.mixins import GroupPermissionMixin


class ProductionListView(GroupPermissionMixin, FormView):
    template_name = 'production/list.html'
    form_class = ReportForm
    permission_required = 'view_production'

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
                    filters &= Q(start_date__range=[start_date, end_date])
                for i in Production.objects.filter(filters):
                    data.append(i.as_dict())
            elif action == 'search_contract':
                data = []
                for i in ProductionContract.objects.filter(production_id=request.POST['id']):
                    data.append(i.as_dict())
            elif action == 'search_supply':
                data = []
                for i in ProductionResource.objects.filter(production_id=request.POST['id'], resource__is_equipment=False):
                    data.append(i.as_dict())
            elif action == 'search_equipment':
                data = []
                for i in ProductionResource.objects.filter(production_id=request.POST['id'], resource__is_equipment=True):
                    data.append(i.as_dict())
            elif action == 'search_plant':
                data = []
                for i in ProductionPlant.objects.filter(production_id=request.POST['id']):
                    data.append(i.as_dict())
            elif action == 'inactivate_production':
                production = Production.objects.get(id=request.POST['id'])
                production.active = False
                production.save()
            elif action == 'activate_production':
                production = Production.objects.get(id=request.POST['id'])
                production.active = True
                production.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Producciones'
        context['create_url'] = reverse_lazy('production_create')
        return context


class ProductionCreateView(GroupPermissionMixin, CreateView):
    model = Production
    template_name = 'production/create.html'
    form_class = ProductionForm
    success_url = reverse_lazy('production_list')
    permission_required = 'add_production'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    detail_json = json.loads(request.POST['detail'])
                    production = Production.objects.create(start_date=request.POST['start_date'], end_date=request.POST['end_date'])
                    for contract in detail_json['contracts']:
                        ProductionContract.objects.create(production_id=production.id, contract_id=int(contract['id']))
                    for supply in detail_json['supplies']:
                        resource = Resource.objects.get(id=int(supply['id']))
                        quantity = int(supply['quantity'])
                        for inventory in Inventory.objects.filter(resource_id=resource.id, saldo__gt=0, active=True).order_by('purchase__date_joined'):
                            detail = ProductionResource(production_id=production.id, inventory_id=inventory.id, resource_id=inventory.resource_id, price=inventory.price)
                            if inventory.saldo >= quantity:
                                detail.quantity = quantity
                                detail.save()
                                detail.inventory.saldo -= quantity
                                detail.inventory.save()
                                quantity = 0
                            else:
                                detail.quantity = inventory.saldo
                                detail.save()
                                quantity -= inventory.saldo
                                detail.inventory.saldo = 0
                                detail.inventory.save()
                            if quantity == 0:
                                break
                    for inventory in detail_json['equipment']:
                        inventory = Inventory.objects.get(id=inventory['id'])
                        ProductionResource.objects.create(production_id=production.id, inventory_id=inventory.id, resource_id=inventory.resource_id, quantity=production.days, price=inventory.depreciation)
                    for plant in detail_json['plants']:
                        ProductionPlant.objects.create(production_id=production.id, plant_id=int(plant['id']), quantity=1)
                    lots = production.productionplant_set.values_list('plant__lot', flat=True).distinct()
                    production.lots.add(*lots)
            elif action == 'search_contract':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                filters = Q(active=True)
                if len(term):
                    filters &= Q(Q(employee__names__icontains=term) | Q(employee__dni__icontains=term))
                queryset = Contract.objects.filter(filters).exclude(id__in=ids).order_by('employee__names')
                if filters.children and len(term):
                    queryset = queryset[0:10]
                for i in queryset:
                    data.append(i.as_dict())
            elif action == 'search_supply':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                filters = Q(is_equipment=False)
                if len(term):
                    filters &= Q(Q(name__icontains=term) | Q(code__icontains=term))
                queryset = Resource.objects.filter(filters).exclude(id__in=ids).order_by('name')
                if filters.children and len(term):
                    queryset = queryset[0:10]
                for i in queryset:
                    if i.stock:
                        data.append(i.as_dict())
            elif action == 'search_equipment':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                filters = Q(resource__is_equipment=True, saldo__gt=0, active=True)
                if len(term):
                    filters &= Q(Q(resource__name__icontains=term) | Q(resource__code__icontains=term) | Q(serie__icontains=term))
                queryset = Inventory.objects.filter(filters).exclude(id__in=ids).order_by('resource__name')
                if filters.children and len(term):
                    queryset = queryset[0:10]
                for i in queryset:
                    data.append(i.as_dict())
            elif action == 'search_plant':
                data = []
                ids = json.loads(request.POST['ids'])
                exclude_id = list(ProductionPlant.objects.filter(production__active=True).values_list('plant_id', flat=True).distinct())
                term = request.POST['term']
                filters = Q(status=PLANT_STATUS[-1][0])
                if len(term):
                    filters &= Q(Q(plant_type__name__icontains=term) | Q(code__icontains=term))
                queryset = Plant.objects.filter(filters).exclude(id__in=exclude_id).exclude(id__in=ids).order_by('plant_type__name')
                if filters.children and len(term):
                    queryset = queryset[0:10]
                for i in queryset:
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Producción'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ProductionDeleteView(GroupPermissionMixin, DeleteView):
    model = Production
    template_name = 'delete.html'
    success_url = reverse_lazy('production_list')
    permission_required = 'delete_production'

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
