from django.forms import ModelForm
from main.models import Equipment

class NewEquipment(ModelForm):
    class Meta:
        model = Equipment
        # fields = ['name', 'location', 'quantity']