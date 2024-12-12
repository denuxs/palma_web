from django import forms

from .models import *
from ..security.forms import update_form_fields_attributes


class CompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Company
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProviderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Provider
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                instace = super().save()
                data = instace.as_dict()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                instace = super().save()
                data = instace.as_dict()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Employee
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Activity
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class LotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['code'].widget.attrs['autofocus'] = True

    class Meta:
        model = Lot
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TapeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self, exclude_fields=['description', 'week'])
        self.fields['color'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tape
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': '3'}),
            'week': forms.TextInput()
        }
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TypeExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = TypeExpense
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ExpensesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self, exclude_fields=['description', 'valor'])
        self.fields['type_expense'].widget.attrs['autofocus'] = True

    class Meta:
        model = Expenses
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': '3'}),
            'valor': forms.TextInput()
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ContractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self, exclude_fields=['salary'])
        self.fields['employee'].widget.attrs['autofocus'] = True

    class Meta:
        model = Contract
        fields = '__all__'
        widgets = {
            'salary': forms.TextInput()
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ResourceTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ResourceType
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self, exclude_fields=['price'])
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Resource
        fields = '__all__'
        widgets = {
            'price': forms.TextInput()
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PurchaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        disabled_fields = kwargs.pop('disabled_fields', [])
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self, exclude_fields=['serie'])
        for field_name in disabled_fields:
            self.fields[field_name].disabled = True
        self.fields['provider'].queryset = Provider.objects.none()

    class Meta:
        model = Purchase
        fields = '__all__'

    serie = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese una serie'
    }), max_length=20, label='Código de serie')


class PlantTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self, exclude_fields=['description'])
        self.fields['code'].widget.attrs['autofocus'] = True

    class Meta:
        model = PlantType
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': '3'}),
        }
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PlantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['plant_type'].widget.attrs['autofocus'] = True

    class Meta:
        model = Plant
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self, exclude_fields=['start_date', 'end_date'])
        self.fields['date_range'].widget.attrs['autofocus'] = True

    class Meta:
        model = Production
        fields = '__all__'

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Buscar por rango de fechas')


class TapeAssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['production_plant'].widget.attrs['autofocus'] = True

    class Meta:
        model = TapeAssignment
        fields = '__all__'

    production = forms.ModelChoiceField(queryset=Production.objects.filter(), label='Producción')


class ActivityControlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['tape_assignment'].widget.attrs['autofocus'] = True

    class Meta:
        model = ActivityControl
        fields = '__all__'

    production = forms.ModelChoiceField(queryset=Production.objects.filter(), label='Producción')


class TapedFruitControlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['tape_assignment'].widget.attrs['autofocus'] = True

    class Meta:
        model = TapedFruitControl
        fields = '__all__'

    production = forms.ModelChoiceField(queryset=Production.objects.filter(), label='Producción')


class HarvestControlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['date_joined'].widget.attrs['autofocus'] = True

    class Meta:
        model = HarvestControl
        fields = '__all__'
        widgets = {
            'observations': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': '3'}),
        }

    production = forms.ModelChoiceField(queryset=Production.objects.filter(), label='Producción')


class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        disabled_fields = kwargs.pop('disabled_fields', [])
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        for field_name in disabled_fields:
            self.fields[field_name].disabled = True
        self.fields['client'].queryset = Client.objects.none()

    class Meta:
        model = Invoice
        fields = '__all__'
