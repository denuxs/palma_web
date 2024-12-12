from django import forms

from core.pos.models import Production, Tape, Activity


class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Buscar por rango de fechas')

    production = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Production.objects.filter(), label='Producción')

    tape = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Tape.objects.filter(), label='Cinta')

    activity = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%;'
    }), queryset=Activity.objects.filter(), label='Actividad')
