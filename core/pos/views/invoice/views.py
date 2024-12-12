import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, TemplateView

from core.pos import printer
from core.pos.forms import InvoiceForm, ClientForm, Invoice, InvoiceDetail, Client, PlantType, HarvestControlDetail, InvoiceHarvestControlDetail
from core.pos.models import Company
from core.reports.forms import ReportForm
from core.security.mixins import GroupPermissionMixin


class InvoiceListView(GroupPermissionMixin, FormView):
    template_name = 'invoice/list.html'
    form_class = ReportForm
    permission_required = 'view_invoice'

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
                for i in Invoice.objects.filter(filters):
                    data.append(i.as_dict())
            elif action == 'search_detail':
                data = []
                for i in InvoiceDetail.objects.filter(invoice_id=request.POST['id']):
                    data.append(i.as_dict())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('invoice_create')
        return context


class InvoiceCreateView(GroupPermissionMixin, CreateView):
    model = Invoice
    template_name = 'invoice/create.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('invoice_list')
    permission_required = 'add_invoice'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['disabled_fields'] = ['subtotal', 'tax', 'total_tax', 'total_amount']
        return kwargs

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    detail = json.loads(request.POST['detail'])
                    invoice = Invoice()
                    invoice.company = Company.objects.first()
                    invoice.client_id = int(request.POST['client'])
                    invoice.date_joined = request.POST['date_joined']
                    invoice.tax = float(detail['tax']) / 100
                    invoice.save()
                    for plant in detail['plants']:
                        plant_type = PlantType.objects.get(id=plant['id'])
                        quantity = int(plant['quantity'])
                        invoice_detail = InvoiceDetail.objects.create(invoice_id=invoice.id, plant_type_id=plant_type.id, quantity=quantity, price=float(plant['price']))
                        for harvest_control_detail in HarvestControlDetail.objects.filter(plant_type_id=plant_type.id, saldo__gt=0, active=True).order_by('harvest_control__date_joined'):
                            detail = InvoiceHarvestControlDetail(invoice_detail_id=invoice_detail.id, harvest_control_detail_id=harvest_control_detail.id)
                            if harvest_control_detail.saldo >= quantity:
                                detail.quantity = quantity
                                detail.save()
                                detail.harvest_control_detail.saldo -= quantity
                                detail.harvest_control_detail.save()
                                quantity = 0
                            else:
                                detail.quantity = harvest_control_detail.saldo
                                detail.save()
                                quantity -= harvest_control_detail.saldo
                                detail.harvest_control_detail.saldo = 0
                                detail.harvest_control_detail.save()
                            if quantity == 0:
                                break
                    invoice.calculate_detail()
                    invoice.calculate_invoice()
            elif action == 'search_plant':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                filters = Q()
                if len(term):
                    filters &= Q(Q(name__icontains=term) | Q(category__icontains=term) | Q(code__icontains=term))
                queryset = PlantType.objects.filter(filters).exclude(id__in=ids).order_by('name')
                if filters.children and len(term):
                    queryset = queryset[0:10]
                for i in queryset:
                    if i.stock:
                        data.append(i.as_dict())
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                for i in Client.objects.filter(Q(names__icontains=term) | Q(dni__icontains=term)).order_by('names')[0:10]:
                    data.append(i.as_dict())
            elif action == 'validate_client':
                field = request.POST['field']
                filters = Q()
                if field == 'names':
                    filters &= Q(names__iexact=request.POST['names'])
                elif field == 'dni':
                    filters &= Q(dni__iexact=request.POST['dni'])
                elif field == 'mobile':
                    filters &= Q(mobile__iexact=request.POST['mobile'])
                elif field == 'email':
                    filters &= Q(email__iexact=request.POST['email'])
                data['valid'] = not Client.objects.filter(filters).exists() if filters.children else True
            elif action == 'create_client':
                form = ClientForm(request.POST)
                data = form.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Venta'
        context['frmClient'] = ClientForm()
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class InvoiceDeleteView(GroupPermissionMixin, DeleteView):
    model = Invoice
    template_name = 'delete.html'
    success_url = reverse_lazy('invoice_list')
    permission_required = 'delete_invoice'

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


class InvoicePrintView(GroupPermissionMixin, TemplateView):
    template_name = 'invoice/ticket.html'
    success_url = reverse_lazy('invoice_list')
    permission_required = 'print_invoice'

    def get(self, request, *args, **kwargs):
        try:
            invoice = Invoice.objects.filter(id=self.kwargs['pk']).first()
            context = {'invoice': invoice, 'height': 300 + invoice.invoicedetail_set.all().count() * 10}
            pdf_file = printer.create_pdf(context=context, template_name=self.template_name)
            return HttpResponse(pdf_file, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(self.success_url)
