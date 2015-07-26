from django.forms import ModelForm
from models import Equipment, Harvest

class NewEquipment(ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'

class NewHarvest(ModelForm):
    class Meta:
        model = Harvest
        fields = '__all__'
