from django import forms
from functools import partial
from models import Equipment, Harvest

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class NewEquipment(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'

class NewHarvest(forms.Form):
    scheduled_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Harvest
        fields = '__all__'
