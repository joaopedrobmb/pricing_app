from django import forms
from django.forms import inlineformset_factory
from .models import QuotationRequests, Equipment

class QuotationRequestForm(forms.ModelForm):
    class Meta:
        model = QuotationRequests
        fields = '__all__'

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['equipment_type','equipment_model' ,'quantity', 'price']

EquipmentFormSet = inlineformset_factory(
    QuotationRequests, Equipment, form=EquipmentForm, extra=1)