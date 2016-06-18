from django import forms
from dal import autocomplete
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div
from harvest.models import *
from member.models import *


class RequestForm(forms.ModelForm):
    class Meta:
        model = RequestForParticipation
        fields = [
            'number_of_people',
            'first_time_picker',
            'helper_picker',
            'picker',
            'phone'
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]

        widgets = {
            'content': forms.Textarea(
                attrs={
                    'placeholder': _(u"Your comment here.")
                }
            ),
        }


class NewHarvest(forms.ModelForm):

    class Meta:
        model = Harvest
        fields = '__all__'

    # """ Determines if this harvest appears on public calendar. """
    is_active = forms.BooleanField()
    status = forms.ChoiceField()
    property = forms.ModelChoiceField(
        queryset=Property.objects.all()
    )
    leader = forms.ModelChoiceField(
        queryset=Person.objects.all()
    )
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    nb_required_pickers = forms.IntegerField()
    pickers = forms.ModelMultipleChoiceField(
        queryset=Person.objects.all()
    )
    equipment_reserved = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.all()
    )
    owner_present = forms.BooleanField()
    owner_help = forms.BooleanField()
    owner_fruit = forms.BooleanField()
    about = forms.CharField(
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super(NewHarvest, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                '',
                # fieldset title

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
                        Field('start_date'), css_class='col-lg-6'
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
        fields = [
            'picker',
            'phone'
        ]


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = [
            'image'
        ]


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('__all__')
        widgets = {
            'owner': autocomplete.ModelSelect2(
               'actor-autocomplete'
            ),
            'trees': autocomplete.ModelSelect2Multiple(
                'tree-autocomplete'
            ),
            'about': forms.Textarea(),
            'avg_nb_required_pickers': forms.NumberInput()
        }


class HarvestForm(forms.ModelForm):
    class Meta:
        model = Harvest
        fields = ('__all__')
        widgets = {
            'trees': autocomplete.ModelSelect2Multiple(
                'tree-autocomplete'
            ),
            'pickers': autocomplete.ModelSelect2Multiple(
                'person-autocomplete'
            ),
            'pick_leader': autocomplete.ModelSelect2(
                'pickleader-autocomplete'
            ),
            'equipment_reserved': autocomplete.ModelSelect2Multiple(
                'equipment-autocomplete'
            ),
            'property': autocomplete.ModelSelect2(
                'property-autocomplete'
            ),
            'nb_required_pickers': forms.NumberInput()
        }


class HarvestYieldForm(forms.ModelForm):
    class Meta:
        model = HarvestYield
        fields = ('__all__')
        widgets = {
            'recipient': autocomplete.ModelSelect2(
                'actor-autocomplete'
            ),
            'tree': autocomplete.ModelSelect2(
                'tree-autocomplete'
            ),
        }


class EquipmentForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(EquipmentForm, self).clean()

        if not (bool(self.cleaned_data['property']) != bool(self.cleaned_data['owner'])):
            raise forms.ValidationError, 'Fill in one of the two fields: property or owner.'

        return cleaned_data

    class Meta:
        model = Equipment
        widgets = {
            'property': autocomplete.ModelSelect2(
                'property-autocomplete'
            ),
            'owner': autocomplete.ModelSelect2(
                'actor-autocomplete'
            ),
        }
        fields = ('__all__')

