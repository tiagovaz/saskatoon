from django import forms
from dal import autocomplete

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Field, Div
from models import *

class NewEquipment(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'

class NewHarvest(forms.ModelForm):

    class Meta:
        model = Harvest
        fields = '__all__'

    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    comment = forms.CharField(widget=forms.Textarea)
    leader = forms.ModelChoiceField (queryset=Person.objects.all())
    scheduled_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    property = forms.ModelChoiceField (queryset=Property.objects.all())
    nb_required_pickers = forms.IntegerField()
    pickers = forms.ModelMultipleChoiceField(queryset=Person.objects.all())
    equipment_reserved = forms.ModelMultipleChoiceField(queryset=Equipment.objects.all())
    # """ Determines if this harvest appears on public calendar. """
    #published = forms.BooleanField()
    status = forms.ModelChoiceField(queryset=Status.objects.all())


    def __init__(self, *args, **kwargs):
        super(NewHarvest, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                '', #fieldset title

                Div(
                    Div(
                        Div('title', css_class='col-lg-12'),
                        css_class='row'
                    ),
                    Div(
                            Field('description', rows="4")
                         ),
                    Div(
                            Field('comment', css_class='col-lg-12', rows="4")
                         ),
                    css_class='col-lg-6'
                ),


                Div(
                    Div(
                        Field('scheduled_date'), css_class='col-lg-6'
                    ),
                    Div(
                        Field('end_date'), css_class='col-lg-6',
                        ),
                    css_class='col-lg-6'
                ),

                Div(
                    Div('leader', css_class='col-lg-6'),
                    Div('property', css_class='col-lg-6'),
                    css_class='col-lg-6'
                ),

                Div(
                    Div('status', css_class='col-lg-6'),
                    Div('nb_required_pickers', css_class='col-lg-6'),
                    Div('equipment_reserved', css_class='col-lg-6'),
                    Div('pickers', css_class='col-lg-6'),
                    css_class='col-lg-6'
                ),

            ),
            Div(
                ButtonHolder(
                    Submit('submit', 'Submit')
                ),
                css_class='col-lg-12'
            )
        )


class RFPForm(forms.ModelForm):
    class Meta:
        model = RequestForParticipation
        fields = ('__all__')
        widgets = {
#            'pickers': autocomplete.ModelSelect2Multiple(
            'picker': autocomplete.ModelSelect2(
                'person-autocomplete'
            )
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('__all__')
        widgets = {
           'trees': autocomplete.ModelSelect2Multiple(
                'tree-autocomplete'
            )
        }
