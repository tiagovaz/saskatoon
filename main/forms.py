from django.forms import ModelForm
from main.models import Equipment, Harvest

class NewEquipment(ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'location', 'quantity']

class NewHarvest(ModelForm):
    class Meta:
        model = Harvest
        # fields = ['name', 'location', 'quantity']