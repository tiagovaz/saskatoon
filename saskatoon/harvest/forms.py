from django import forms
from dal import autocomplete
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div
from harvest.models import *
from member.models import *

class RequestForm(forms.ModelForm):
    picker_email = forms.EmailField(help_text='Enter a valid email address, please.')
    picker_first_name = forms.CharField(label='First name')
    picker_family_name = forms.CharField(label='Family name')
    picker_phone = forms.CharField(label='Phone')
    harvest_id = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        email = self.cleaned_data['picker_email']
        auth_user_count = AuthUser.objects.filter(email=email).count()
        if auth_user_count > 0: # check if email is already in the database
            auth_user = AuthUser.objects.get(email=email)
            harvest_obj = Harvest.objects.get(id=self.cleaned_data['harvest_id'])
            request_same_user_count = RequestForParticipation.objects.filter(picker = auth_user.person, harvest = harvest_obj).count()
            if request_same_user_count > 0: # check if email has requested for the same harvest
                raise forms.ValidationError, 'You have already requested to join this pick.'

    def save(self):
        instance = super(RequestForm, self).save(commit=False)

        first_name = self.cleaned_data['picker_first_name']
        family_name = self.cleaned_data['picker_family_name']
        phone = self.cleaned_data['picker_phone']
        email = self.cleaned_data['picker_email']
        harvest_obj = Harvest.objects.get(id=self.cleaned_data['harvest_id'])

        # check if the email is already registered
        auth_user_count = AuthUser.objects.filter(email = email).count()

        if auth_user_count > 0: # user is already in the database
            auth_user = AuthUser.objects.get(email=email)
            instance.picker = auth_user.person
            instance.harvest = harvest_obj
        else: # user is not in the database, so create a new one and link it to Person obj
            instance.picker = Person.objects.create(first_name=first_name, family_name=family_name, phone=phone)
            auth_user = AuthUser.objects.create(email=email, person=instance.picker)

        instance.save()
        return instance

    class Meta:
        model = RequestForParticipation
        fields = [
            'number_of_people',
            'first_time_picker',
            'helper_picker',
            'picker_first_name',
            'picker_family_name',
            'picker_email',
            'picker_phone',
            'comment',
            'harvest_id'
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
    status = forms.ModelChoiceField(
        queryset=HarvestStatus.objects.all()
    )
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

# Used in admin interface
class RFPForm(forms.ModelForm):
    class Meta:
        model = RequestForParticipation
        fields = '__all__'

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

