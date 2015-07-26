from django import forms
from models import *

class NewEquipment(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'



class NewHarvest(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(max_length=1000, widget=forms.Textarea)
    leader = forms.ModelChoiceField (queryset=Person.objects.all())
    scheduled_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    #property = forms.ModelChoiceField (queryset=Property.objects.all())
    nb_required_pickers = forms.IntegerField()
    pickers = forms.ModelMultipleChoiceField(queryset=Person.objects.all())
    equipment_reserved = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all())
    """ Determines if this harvest appears on public calendar. """
    published = forms.BooleanField()
    status = forms.ModelChoiceField(queryset=Status.objects.all())