import django_filters
from harvest.models import Harvest, HARVESTS_STATUS_CHOICES
from member.models import AuthUser, Neighborhood
from django import forms
from django_filters import FilterSet, ChoiceFilter, ModelChoiceFilter, NumberFilter

FILTER_HARVEST_CHOICES = list(HARVESTS_STATUS_CHOICES)
FILTER_HARVEST_CHOICES.insert(0, ('', '---------'))


class HarvestFilter(FilterSet):
    seasons = []

    class Meta:
        model = Harvest
        fields = {
            'status': ['exact'],
            'pick_leader': ['exact'],
            'trees': ['exact'],
            'property__neighborhood':['exact'],
            'start_date': ['exact']
        }

    def __init__(self, *args, **kwargs):
        """Return a list of years based on past and current harvests dates"""
        super(HarvestFilter, self).__init__(*args, **kwargs)
        seasons = []
        for y in Harvest.objects.all():
            if y.start_date != None:
                t_seasons = (y.start_date.strftime("%Y"), y.start_date.strftime("%Y"))
                seasons.append(t_seasons)
        seasons.insert(0, ('', '---------'))
        self.seasons = seasons

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
        choices=seasons,
        label="Season",
        lookup_expr=('year')
    )

