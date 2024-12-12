from django import forms

from .models import *


def update_form_fields_attributes(form, exclude_fields=None):
    if not exclude_fields:
        exclude_fields = []
    for object_field in form.visible_fields():
        if object_field.name in exclude_fields:
            continue
        if isinstance(object_field.field, forms.IntegerField):
            object_field.field.widget = forms.TextInput(attrs={'class': 'form-control only-numbers', 'autocomplete': 'off', 'placeholder': object_field.help_text})
        elif isinstance(object_field.field, (forms.DecimalField)):
            object_field.field.widget.attrs.update({'class': 'form-control only-decimals'})
        elif isinstance(object_field.field, (forms.CharField, forms.GenericIPAddressField)):
            object_field.field.widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'placeholder': object_field.help_text})
        elif isinstance(object_field.field, (forms.ModelChoiceField, forms.TypedChoiceField, forms.ChoiceField)):
            object_field.field.widget.attrs.update({'class': 'form-control select2', 'style': 'width: 100%;'})
        elif isinstance(object_field.field, forms.DateField):
            object_field.field.widget.attrs.update({'class': 'form-control', 'id': object_field.name, 'value': datetime.now().strftime('%Y-%m-%d'), 'data-toggle': 'datetimepicker', 'data-target': f'#{object_field.name}'})
            object_field.field.widget.format = '%Y-%m-%d'
        elif isinstance(object_field.field, forms.BooleanField):
            object_field.field.widget.attrs.update({'class': 'form-control-checkbox'})
        elif isinstance(object_field.field, (forms.ImageField, forms.FileField)):
            object_field.field.widget.attrs.update({'class': 'form-control'})


def update_field_class(field, name):
    attrs = field.widget.attrs
    class_value = attrs.get('class', '')
    class_value += f' {name}'
    attrs['class'] = class_value


class ModuleTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ModuleType
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


class ModuleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self, exclude_fields=['module_type', 'permissions'])
        self.fields['url'].widget.attrs['autofocus'] = True

    class Meta:
        model = Module
        fields = '__all__'
        widgets = {
            'permissions': forms.SelectMultiple(attrs={'class': 'form-control select2', 'multiple': 'multiple', 'style': 'width:100%'}),
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


class GroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Group
        fields = 'name',
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre', 'class': 'form-control'}),
        }


class DashboardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_form_fields_attributes(self)
        self.fields['layout'].widget.attrs['autofocus'] = True

    class Meta:
        model = Dashboard
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
