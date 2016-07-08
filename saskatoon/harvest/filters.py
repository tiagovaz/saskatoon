import django_filters
from models import Harvest, HARVESTS_STATUS_CHOICES
from member.models import AuthUser, Neighborhood
from django import forms
from django_filters import FilterSet, ChoiceFilter, ModelChoiceFilter, NumberFilter

FILTER_HARVEST_CHOICES = list(HARVESTS_STATUS_CHOICES)
FILTER_HARVEST_CHOICES.insert(0, ('', '---------'))

def get_seasons():
    """Return a list of years based on past and current harvests dates"""
    seasons = []
    t_seasons = ()
    for y in Harvest.objects.all():
        if y.start_date != None:
            t_seasons = (y.start_date.strftime("%Y"), y.start_date.strftime("%Y"))
            seasons.append(t_seasons)
    seasons.insert(0, ('', '---------'))
    return set(seasons)

FILTER_HARVEST_SEASONS = get_seasons()

class HarvestFilter(FilterSet):

    class Meta:
        model = Harvest
        fields = {
            'status': ['exact'],
            'pick_leader': ['exact'],
            'trees': ['exact'],
            'property__neighborhood':['exact'],
            'start_date': ['exact']
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

    start_date = ChoiceFilter(
        choices=FILTER_HARVEST_SEASONS,
        label="Season",
        lookup_expr=('year')
    )

