from datetime import datetime

from django.db import models
from django.db.models import Sum, FloatField, IntegerField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.pos.choices import *
from core.user.models import User


class Company(models.Model):
    name = models.CharField(max_length=50, help_text='Ingrese un nombre', verbose_name='Nombre')
    ruc = models.CharField(max_length=13, help_text='Ingrese el ruc de la empresa', verbose_name='Ruc')
    address = models.CharField(max_length=200, help_text='Ingrese una dirección', verbose_name='Dirección')
    mobile = models.CharField(max_length=10, help_text='Ingrese un número de teléfono celular', verbose_name='Teléfono celular')
    phone = models.CharField(max_length=9, help_text='Ingrese un número de teléfono convencional', verbose_name='Teléfono convencional')
    email = models.CharField(max_length=50, help_text='Ingrese un correo electrónico', verbose_name='Email')
    website = models.CharField(max_length=250, help_text='Ingrese una página web', verbose_name='Página web')
    description = models.CharField(max_length=500, null=True, blank=True, help_text='Ingrese una descripción', verbose_name='Descripción')
    image = models.ImageField(null=True, blank=True, upload_to='company/%Y/%m/%d', verbose_name='Logotipo de la empresa')
    tax = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='IVA')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_full_path_image(self):
        if self.image:
            return self.image.path
        return f'{settings.BASE_DIR}{settings.STATIC_URL}img/default/empty.png'

    def get_tax(self):
        return float(self.tax)

    def as_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        default_permissions = ()
        permissions = (
            ('change_company', 'Can change Empresa'),
        )


class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text='Ingrese un nombre', verbose_name='Nombre')
    ruc = models.CharField(max_length=13, unique=True, help_text='Ingrese un número de ruc', verbose_name='Ruc')
    mobile = models.CharField(max_length=10, unique=True, help_text='Ingrese un número de teléfono', verbose_name='Teléfono celular')
    address = models.CharField(max_length=500, null=True, blank=True, help_text='Ingrese una dirección', verbose_name='Dirección')
    email = models.CharField(max_length=50, unique=True, help_text='Ingrese un correo electrónico', verbose_name='Email')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.name} ({self.ruc})'

    def as_dict(self):
        item = model_to_dict(self)
        item['text'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'


class Client(models.Model):
    names = models.CharField(max_length=50, unique=True, help_text='Ingrese un nombre', verbose_name='Nombre')
    dni = models.CharField(max_length=13, unique=True, help_text='Ingrese un número de cedula', verbose_name='Número de cedula')
    mobile = models.CharField(max_length=10, unique=True, help_text='Ingrese un número de teléfono', verbose_name='Teléfono celular')
    address = models.CharField(max_length=500, null=True, blank=True, help_text='Ingrese una dirección', verbose_name='Dirección')
    email = models.CharField(max_length=50, unique=True, help_text='Ingrese un correo electrónico', verbose_name='Email')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.names} ({self.dni})'

    def as_dict(self):
        item = model_to_dict(self)
        item['text'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Employee(models.Model):
    names = models.CharField(max_length=50, unique=True, help_text='Ingrese un nombre', verbose_name='Nombre')
    dni = models.CharField(max_length=13, unique=True, help_text='Ingrese un número de cedula', verbose_name='Número de cedula')
    mobile = models.CharField(max_length=10, unique=True, help_text='Ingrese un número de teléfono', verbose_name='Teléfono celular')
    address = models.CharField(max_length=500, null=True, blank=True, help_text='Ingrese una dirección', verbose_name='Dirección')
    email = models.CharField(max_length=50, unique=True, help_text='Ingrese un correo electrónico', verbose_name='Email')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.names} ({self.dni})'

    def as_dict(self):
        item = model_to_dict(self)
        item['text'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'


class Contract(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Empleado')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
    salary = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Salario')
    active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.employee.names

    def as_dict(self):
        item = model_to_dict(self)
        item['value'] = self.employee.get_full_name()
        item['employee'] = self.employee.as_dict()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['salary'] = float(self.salary)
        return item

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'


class Activity(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text='Ingrese un nombre', verbose_name='Nombre')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.name

    def as_dict(self):
        item = model_to_dict(self)
        item['text'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['name']


class Lot(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text='Ingrese un código', verbose_name='Código')
    name = models.CharField(max_length=50, help_text='Ingrese un nombre', verbose_name='Nombre')

    def __str__(self):
        return f'{self.name} ({self.code})'

    def as_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'


class Tape(models.Model):
    color = models.CharField(max_length=50, help_text='Ingrese un color', verbose_name='Color de la cinta')
    name = models.CharField(max_length=500, help_text='Ingrese un nombre', verbose_name='Nombre')
    description = models.CharField(max_length=500, null=True, blank=True, help_text='Ingrese una descripción', verbose_name='Descripción')
    week = models.PositiveIntegerField(default=0, unique=True, verbose_name='Semana')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.name} ({self.week})'

    def as_dict(self):
        item = model_to_dict(self)
        item['text'] = self.get_full_name()
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cinta'
        verbose_name_plural = 'Cintas'
        ordering = ['week']


class TypeExpense(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text='Ingrese un nombre', verbose_name='Nombre')

    def __str__(self):
        return self.name

    def as_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Gasto'
        verbose_name_plural = 'Tipos de Gastos'
        default_permissions = ()
        permissions = (
            ('view_type_expense', 'Can view Tipo de Gasto'),
            ('add_type_expense', 'Can add Tipo de Gasto'),
            ('change_type_expense', 'Can change Tipo de Gasto'),
            ('delete_type_expense', 'Can delete Tipo de Gasto'),
        )


class Expenses(models.Model):
    type_expense = models.ForeignKey(TypeExpense, on_delete=models.PROTECT, verbose_name='Tipo de Gasto')
    description = models.CharField(max_length=500, null=True, blank=True, help_text='Ingrese los detalles (opcional)', verbose_name='Detalles')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return self.description

    def as_dict(self):
        item = model_to_dict(self)
        item['type_expense'] = self.type_expense.as_dict()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['valor'] = float(self.valor)
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.description is None:
            self.description = 's/n'
        elif len(self.description) == 0:
            self.description = 's/n'
        super(Expenses, self).save()

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'


class ResourceType(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text='Ingrese un nombre', verbose_name='Nombre')

    def __str__(self):
        return self.name

    def as_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Recurso'
        verbose_name_plural = 'Tipos de Insumos'
        default_permissions = ()
        permissions = (
            ('view_resource_type', 'Can view Tipo de Recurso'),
            ('add_resource_type', 'Can add Tipo de Recurso'),
            ('change_resource_type', 'Can change Tipo de Recurso'),
            ('delete_resource_type', 'Can delete Tipo de Recurso'),
        )


class Resource(models.Model):
    name = models.CharField(max_length=150, help_text='Ingrese un nombre', verbose_name='Nombre')
    code = models.CharField(max_length=20, unique=True, help_text='Ingrese un código', verbose_name='Código')
    resource_type = models.ForeignKey(ResourceType, on_delete=models.PROTECT, verbose_name='Tipo de recurso')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio')
    image = models.ImageField(upload_to='resource/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    is_equipment = models.BooleanField(default=False, verbose_name='¿Es un equipo?')

    def __str__(self):
        return self.get_full_name()

    @property
    def stock(self):
        return int(self.inventory_set.all().aggregate(result=Coalesce(Sum('saldo'), 0, output_field=IntegerField()))['result'])

    def get_full_name(self):
        return f'{self.name} ({self.code}) ({self.resource_type.name})'

    def get_short_name(self):
        return f'{self.name} ({self.resource_type.name})'

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def as_dict(self):
        item = model_to_dict(self)
        item['value'] = self.get_full_name()
        item['stock'] = self.stock
        item['full_name'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['resource_type'] = self.resource_type.as_dict()
        item['price'] = float(self.price)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'


class Purchase(models.Model):
    number = models.CharField(max_length=8, unique=True, help_text='Ingrese un número de factura', verbose_name='Número de factura')
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, verbose_name='Proveedor')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='IVA')
    total_tax = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Total de IVA')
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Total a pagar')

    def __str__(self):
        return self.provider.name

    def calculate_detail(self):
        for detail in self.inventory_set.filter():
            detail.subtotal = float(detail.price) * detail.quantity
            detail.save()

    def calculate_invoice(self):
        self.subtotal = float(self.inventory_set.all().aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField()))['result'])
        self.total_tax = float(self.subtotal) * float(self.tax)
        self.total_amount = float(self.subtotal) + float(self.total_tax)
        self.save()

    def as_dict(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['provider'] = self.provider.as_dict()
        item['subtotal'] = float(self.subtotal)
        item['tax'] = float(self.tax)
        item['total_tax'] = float(self.total_tax)
        item['total_amount'] = float(self.total_amount)
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        default_permissions = ()
        permissions = (
            ('view_purchase', 'Can view Compra'),
            ('add_purchase', 'Can add Compra'),
            ('delete_purchase', 'Can delete Compra'),
        )


class Inventory(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT)
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    guarantee = models.IntegerField(default=0)
    saldo = models.IntegerField(default=0)
    serie = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.resource.name

    @property
    def depreciation(self):
        amount = (float(self.price) / int(self.guarantee)) / 365
        return float(amount)

    def as_dict(self):
        item = model_to_dict(self, exclude=['purchase'])
        item['value'] = f'{self.resource.get_full_name()} - {self.serie}'
        item['resource'] = self.resource.as_dict()
        item['price'] = float(self.price)
        item['subtotal'] = float(self.subtotal)
        return item

    def edit(self):
        super(Inventory, self).save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            self.saldo = self.quantity
        self.active = self.saldo > 0
        super(Inventory, self).save()

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        default_permissions = ()


class PlantType(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text='Ingrese un código', verbose_name='Código')
    name = models.CharField(max_length=100, unique=True, help_text='Ingrese un nombre', verbose_name='Nombre')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio')
    category = models.CharField(max_length=10, choices=PLANT_CATEGORY, verbose_name='Tipo')
    description = models.CharField(max_length=500, blank=True, null=True, help_text='Ingrese una descripción', verbose_name='Descripción')

    def __str__(self):
        return self.name

    @property
    def stock(self):
        return int(self.harvestcontroldetail_set.all().aggregate(result=Coalesce(Sum('saldo'), 0, output_field=IntegerField()))['result'])

    def as_dict(self):
        item = model_to_dict(self)
        item['value'] = self.name
        item['stock'] = self.stock
        item['price'] = float(self.price)
        item['category'] = {'id': self.category, 'name': self.get_category_display()}
        return item

    class Meta:
        verbose_name = 'Tipo de Planta'
        verbose_name_plural = 'Tipo de Plantas'
        default_permissions = ()
        permissions = (
            ('view_plant_type', 'Can view Tipo de Planta'),
            ('add_plant_type', 'Can add Tipo de Planta'),
            ('change_plant_type', 'Can change Tipo de Planta'),
            ('delete_plant_type', 'Can delete Tipo de Planta'),
        )


class Plant(models.Model):
    plant_type = models.ForeignKey(PlantType, on_delete=models.PROTECT, verbose_name='Tipo de Planta')
    lot = models.ForeignKey(Lot, on_delete=models.PROTECT, verbose_name='Lote')
    code = models.CharField(max_length=20, unique=True, help_text='Ingrese un código', verbose_name='Código')
    latitude = models.CharField(max_length=30, help_text='Ingrese una latitud', verbose_name='Latitud')
    longitude = models.CharField(max_length=30, help_text='Ingrese una longitud', verbose_name='Longitud')
    status = models.CharField(max_length=10, choices=PLANT_STATUS, default=PLANT_STATUS[0][0], verbose_name='Estado')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.plant_type.name} ({self.code}) - {self.lot.name} = {self.latitude} / {self.longitude}'

    def get_short_name(self):
        return f'{self.plant_type.name} - {self.code} | ({self.latitude}, {self.longitude})'

    def as_dict(self):
        item = model_to_dict(self)
        item['value'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['plant_type'] = self.plant_type.as_dict()
        item['lot'] = self.lot.as_dict()
        item['status'] = {'id': self.status, 'name': self.get_status_display()}
        return item

    class Meta:
        verbose_name = 'Planta'
        verbose_name_plural = 'Plantas'


class Production(models.Model):
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    lots = models.ManyToManyField(Lot)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name()

    @property
    def number(self):
        return f'{self.id:06d}'

    @property
    def days(self):
        start_date = self.start_date
        end_date = self.end_date
        if isinstance(self.start_date, str):
            start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        if isinstance(self.end_date, str):
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        return (end_date - start_date).days + 1

    @property
    def lots_text(self):
        return ','.join([lot.name for lot in self.lots.all()])

    def formatted_start_date(self):
        return self.start_date.strftime('%Y-%m-%d')

    def formatted_end_date(self):
        return self.end_date.strftime('%Y-%m-%d')

    def get_full_name(self):
        return f'Número: {self.number} / Lotes: {self.lots_text} / Fecha de inicio: {self.formatted_start_date()} / Fecha de fin: {self.formatted_end_date()} / Estado: {self.get_active_display()}'

    def get_short_name(self):
        return f'Número: {self.number} / Fecha de inicio: {self.formatted_start_date()} / Fecha de fin: {self.formatted_end_date()} / Estado: {self.get_active_display()}'

    def get_active_display(self):
        return 'Activa' if self.active else 'Inactiva'

    def as_dict(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['lots_text'] = self.lots_text
        item['number'] = self.number
        item['days'] = self.days
        item['lots'] = [lot.as_dict() for lot in self.lots.all()]
        item['start_date'] = self.formatted_start_date()
        item['end_date'] = self.formatted_end_date()
        return item

    def delete(self, using=None, keep_parents=False):
        for detail in self.productionresource_set.filter(resource__is_equipment=False):
            detail.inventory.saldo += detail.quantity
            detail.inventory.save()
        super(Production, self).delete()

    class Meta:
        verbose_name = 'Producción'
        verbose_name_plural = 'Producciones'
        default_permissions = ()
        permissions = (
            ('view_production', 'Can view Producción'),
            ('add_production', 'Can add Producción'),
            ('delete_production', 'Can delete Producción')
        )


class ProductionContract(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT)

    def __str__(self):
        return self.contract.employee.names

    def as_dict(self):
        item = model_to_dict(self, exclude=['production'])
        item['contract'] = self.contract.as_dict()
        return item

    class Meta:
        verbose_name = 'Contracto de la Producción'
        verbose_name_plural = 'Contractos de la Producción'
        default_permissions = ()


class ProductionResource(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)
    inventory = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.resource.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.subtotal = float(self.price) * self.quantity
        super(ProductionResource, self).save()

    def as_dict(self):
        item = model_to_dict(self, exclude=['production'])
        item['resource'] = self.resource.as_dict()
        item['inventory'] = self.inventory.as_dict()
        item['price'] = float(self.price)
        item['subtotal'] = float(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Recurso de la Producción'
        verbose_name_plural = 'Recursos de la Producción'
        default_permissions = ()


class ProductionPlant(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.plant.__str__()

    def get_tapes(self):
        tapes = Tape.objects.filter().order_by('week')
        tapes_list = [i.as_dict() for i in tapes]
        info = dict()
        previous = self.tapeassignment_set.last()
        info['previous'] = previous.as_dict() if previous else dict()
        next = list(filter(lambda tape: tape['week'] > previous.tape.week, tapes_list)) if previous else []
        next = sorted(next, key=lambda tape: tape['week'])
        info['next'] = next[0] if len(next) else tapes_list[0]
        info['finalized'] = previous.tape.id == tapes.last().id if previous and tapes.exists() else False
        return info

    def as_dict(self):
        item = model_to_dict(self, exclude=['production'])
        item['plant'] = self.plant.as_dict()
        return item

    class Meta:
        verbose_name = 'Planta de la Producción'
        verbose_name_plural = 'Plantas de la Producción'
        default_permissions = ()


class TapeAssignment(models.Model):
    production_plant = models.ForeignKey(ProductionPlant, on_delete=models.CASCADE)
    tape = models.ForeignKey(Tape, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    observations = models.CharField(max_length=500, null=True, blank=True, verbose_name='Detalles')

    def __str__(self):
        return f'Planta: {self.production_plant.plant.__str__()}, Cinta: {self.tape.color}, Semana: {self.tape.week}, Fecha de registro: {self.formatted_date_joined()}'

    @property
    def latest_fruit_control_quantity(self):
        taped_fruit_control = self.tapedfruitcontrol_set.order_by('-id').first()
        if taped_fruit_control:
            return taped_fruit_control.quantity
        return 0

    def formatted_date_joined(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def as_dict(self):
        item = model_to_dict(self)
        item['production_plant'] = self.production_plant.as_dict()
        item['tape'] = self.tape.as_dict()
        item['date_joined'] = self.formatted_date_joined()
        return item

    class Meta:
        verbose_name = 'Asignación de cintas por semana'
        verbose_name_plural = 'Asignaciones de cintas por semana'
        default_permissions = ()
        permissions = (
            ('view_tape_assignment', 'Can view Asignación de cintas por semana'),
            ('add_tape_assignment', 'Can add Asignación de cintas por semana'),
            ('delete_tape_assignment', 'Can delete Asignación de cintas por semana'),
        )


class ActivityControl(models.Model):
    tape_assignment = models.ForeignKey(TapeAssignment, on_delete=models.CASCADE, verbose_name='Asignación de cintas por semana')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='Actividad')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    observations = models.CharField(max_length=5000, null=True, blank=True, help_text='Ingrese una descripción', verbose_name='Observaciones')

    def __str__(self):
        return f'Actividad: {self.activity.name} - R.Cinta: {self.tape_assignment.__str__()} - Fecha de registro: {self.formatted_date_joined()}'

    def formatted_date_joined(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def as_dict(self):
        item = model_to_dict(self)
        item['tape_assignment'] = self.tape_assignment.as_dict()
        item['activity'] = self.activity.as_dict()
        item['date_joined'] = self.formatted_date_joined()
        return item

    class Meta:
        verbose_name = 'Control de Actividades Agronómicas'
        verbose_name_plural = 'Controles de Actividades Agronómicas'
        default_permissions = ()
        permissions = (
            ('view_activity_control', 'Can view Control de Actividades Agronómicas'),
            ('add_activity_control', 'Can add Control de Actividades Agronómicas'),
            ('delete_activity_control', 'Can delete Control de Actividades Agronómicas'),
        )
        ordering = ['-date_joined']


class TapedFruitControl(models.Model):
    tape_assignment = models.ForeignKey(TapeAssignment, on_delete=models.CASCADE, verbose_name='Asignación de cintas por semana')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    quantity = models.IntegerField(default=0, verbose_name='Número de racimos en la planta')
    observations = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Observaciones')

    def __str__(self):
        return f'Cant.Racimos: {self.quantity} - R.Cinta: {self.tape_assignment.__str__()} - Fecha de registro: {self.formatted_date_joined()}'

    def formatted_date_joined(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def as_dict(self):
        item = model_to_dict(self)
        item['tape_assignment'] = self.tape_assignment.as_dict()
        item['date_joined'] = self.formatted_date_joined()
        return item

    class Meta:
        verbose_name = 'Control de Fruta Encintada'
        verbose_name_plural = 'Controles de Fruta Encintada'
        default_permissions = ()
        permissions = (
            ('view_taped_fruit_control', 'Can view Control de Fruta Encintada'),
            ('add_taped_fruit_control', 'Can add Control de Fruta Encintada'),
            ('delete_taped_fruit_control', 'Can delete Control de Fruta Encintada'),
        )
        ordering = ['-date_joined']


class HarvestControl(models.Model):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    production = models.ForeignKey(Production, on_delete=models.CASCADE, verbose_name='Producción')
    total_bunches = models.IntegerField(default=0, verbose_name='Total de racimos cosechados')
    total_boxes = models.IntegerField(default=0, verbose_name='Total de cajas')
    observations = models.CharField(max_length=5000, null=True, blank=True, help_text='Ingrese una descripción', verbose_name='Observaciones')

    def __str__(self):
        return f'Total.Racimos cosechados: {self.total_bunches} - Número de cajas: {self.total_boxes} - Fecha de registro: {self.formatted_date_joined()}'

    def calculate_totals(self):
        self.total_bunches = float(self.harvestcontroldetail_set.all().aggregate(result=Coalesce(Sum('quantity'), 0, output_field=IntegerField()))['result'])
        self.total_boxes = float(self.harvestcontroldetail_set.all().aggregate(result=Coalesce(Sum('boxes'), 0, output_field=IntegerField()))['result'])
        self.save()

    def formatted_date_joined(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def as_dict(self):
        item = model_to_dict(self)
        item['production'] = self.production.as_dict()
        item['date_joined'] = self.formatted_date_joined()
        return item

    class Meta:
        verbose_name = 'Control de Cosecha'
        verbose_name_plural = 'Controles de Cosecha'
        default_permissions = ()
        permissions = (
            ('view_harvest_control', 'Can view Control de Cosecha'),
            ('add_harvest_control', 'Can add Control de Cosecha'),
            ('delete_harvest_control', 'Can delete Control de Cosecha'),
        )


class HarvestControlDetail(models.Model):
    plant_type = models.ForeignKey(PlantType, on_delete=models.CASCADE)
    harvest_control = models.ForeignKey(HarvestControl, on_delete=models.CASCADE)
    tape_assignment = models.ForeignKey(TapeAssignment, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    boxes = models.IntegerField(default=0)
    saldo = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Cantidad: {self.quantity} - Cajas: {self.boxes} - R.Cinta: {self.tape_assignment.__str__()}'

    def as_dict(self):
        item = model_to_dict(self)
        item['plant_type'] = self.plant_type.as_dict()
        item['harvest_control'] = self.harvest_control.as_dict()
        item['tape_assignment'] = self.tape_assignment.as_dict()
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            self.saldo = self.boxes
        self.active = self.saldo > 0
        super(HarvestControlDetail, self).save()

    class Meta:
        verbose_name = 'Detalle de Control de Cosecha'
        verbose_name_plural = 'Detalles de Control de Cosecha'
        default_permissions = ()


class Invoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='Compañia')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Cliente')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Subtotal')
    tax = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='IVA')
    total_tax = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Total de IVA')
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Total a pagar')

    def __str__(self):
        return self.client.names

    @property
    def tax_percent(self):
        return int(self.tax * 100)

    @property
    def number(self):
        return f'{self.id:06d}'

    def calculate_detail(self):
        for detail in self.invoicedetail_set.filter():
            detail.subtotal = float(detail.price) * detail.quantity
            detail.save()

    def calculate_invoice(self):
        self.subtotal = float(self.invoicedetail_set.all().aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField()))['result'])
        self.total_tax = float(self.subtotal) * float(self.tax)
        self.total_amount = float(self.subtotal) + float(self.total_tax)
        self.save()

    def as_dict(self):
        item = model_to_dict(self)
        item['number'] = self.number
        item['client'] = self.client.as_dict()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['subtotal'] = float(self.subtotal)
        item['tax'] = float(self.tax)
        item['total_tax'] = float(self.total_tax)
        item['total_amount'] = float(self.total_amount)
        return item

    def delete(self, using=None, keep_parents=False):
        for detail in InvoiceHarvestControlDetail.objects.filter(invoice_detail__invoice=self):
            detail.harvest_control_detail.saldo += detail.quantity
            detail.harvest_control_detail.save()
        super(Invoice, self).delete()

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        default_permissions = ()
        permissions = (
            ('view_invoice', 'Can view Factura'),
            ('add_invoice', 'Can add Factura'),
            ('delete_invoice', 'Can delete Factura'),
            ('print_invoice', 'Can print Factura'),
        )


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    plant_type = models.ForeignKey(PlantType, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.plant_type.__str__()

    def as_dict(self):
        item = model_to_dict(self, exclude=['invoice'])
        item['plant_type'] = self.plant_type.as_dict()
        item['price'] = float(self.price)
        item['subtotal'] = float(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalle de Facturas'
        default_permissions = ()


class InvoiceHarvestControlDetail(models.Model):
    invoice_detail = models.ForeignKey(InvoiceDetail, on_delete=models.CASCADE)
    harvest_control_detail = models.ForeignKey(HarvestControlDetail, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.harvest_control_detail.__str__()

    def as_dict(self):
        item = model_to_dict(self, exclude=['invoice'])
        item['harvest_control_detail'] = self.harvest_control_detail.as_dict()
        return item

    class Meta:
        verbose_name = 'Detalle de Control de Cosecha Factura'
        verbose_name_plural = 'Detalle de Control de Cosecha Facturas'
        default_permissions = ()
