from django.utils.translation import ugettext_lazy as _
from django_filters import FilterSet, ChoiceFilter, ModelChoiceFilter, BooleanFilter
from django_filters.widgets import BooleanWidget
from harvest.models import Harvest, HARVESTS_STATUS_CHOICES, TreeType, Property
from member.models import AuthUser, Neighborhood

FILTER_HARVEST_CHOICES = list(HARVESTS_STATUS_CHOICES)
FILTER_HARVEST_CHOICES.insert(0, ('', '---------'))

class HarvestFilter(FilterSet):
    seasons = []
    for y in Harvest.objects.all():
        if y.start_date is not None:
            t_seasons = (
                    y.start_date.strftime("%Y"),
                    y.start_date.strftime("%Y")
                )
            seasons.append(t_seasons)
    seasons = list(set(seasons))
    seasons = sorted(seasons, key=lambda tup: tup[1])

    start_date = ChoiceFilter(
        choices=seasons,
        label=_("Season"),
        lookup_expr='year',
        help_text="",
    )

    status = ChoiceFilter(
        choices=FILTER_HARVEST_CHOICES,
        help_text="",
    )

    pick_leader = ModelChoiceFilter(
        queryset=AuthUser.objects.filter(
            is_staff=True
        ),
        required=False,
        help_text="",
    )

    trees = ModelChoiceFilter(
        queryset=TreeType.objects.all(),
        label=_("Tree"),
        help_text="",
        required=False
    )

    property__neighborhood = ModelChoiceFilter(
        queryset=Neighborhood.objects.all(),
        label=_("Neighborhood"),
        help_text="",
        required=False
    )

    class Meta:
        model = Harvest
        fields = {
        'status': ['exact'],
        'pick_leader': ['exact'],
        'trees': ['exact'],
        'property__neighborhood': ['exact'],
        'start_date': ['exact'],
        }


class PropertyFilter(FilterSet):
    neighborhood = ModelChoiceFilter(
        queryset=Neighborhood.objects.all(),
        label=_("Neighborhood"),
        help_text="",
        required=False
    )

    trees = ModelChoiceFilter(
        queryset=TreeType.objects.all(),
        label=_("Tree"),
        help_text="",
        required=False
    )
    is_active = BooleanFilter(help_text="")
    authorized = BooleanFilter(help_text="")
    pending = BooleanFilter(help_text="")
    ladder_available = BooleanFilter(help_text="")
    ladder_available_for_outside_picks = BooleanFilter(help_text="")

    class Meta:
        model = Property
        fields = {
        'neighborhood': ['exact'],
        'trees': ['exact'],
        'is_active':['exact'],
        'authorized':['exact'],
        'pending':['exact'],
        'ladder_available':['exact'],
        'ladder_available_for_outside_picks':['exact']
        }
