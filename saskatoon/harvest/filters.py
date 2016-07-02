import django_filters
from models import Harvest, HARVESTS_STATUS_CHOICES
from member.models import AuthUser, Neighborhood
from django import forms
from django_filters import FilterSet, ChoiceFilter, ModelChoiceFilter

FILTER_HARVEST_CHOICES = list(HARVESTS_STATUS_CHOICES)
FILTER_HARVEST_CHOICES.insert(0, ('', '---------'))


class HarvestFilter(FilterSet):
    class Meta:
        model = Harvest
        fields = {
            'status': ['exact'],
            'pick_leader': ['exact'],
            'trees': ['exact'],
            'property__neighborhood':['exact']
        }

    status = ChoiceFilter(
        choices=FILTER_HARVEST_CHOICES
    )

    pick_leader = ModelChoiceFilter(
        queryset=AuthUser.objects.filter(
            is_staff=True
        ),
        required=False
    )

