from django.utils.translation import ugettext_lazy as _
from django_filters import FilterSet, ChoiceFilter, ModelChoiceFilter
from harvest.models import Harvest, HARVESTS_STATUS_CHOICES
from member.models import AuthUser

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
    seasons.insert(0, ('', '---------'))

    seasons = list(set(seasons))

    start_date = ChoiceFilter(
        choices=seasons,
        label=_("Season"),
        lookup_expr='year',
    )

    status = ChoiceFilter(
        choices=FILTER_HARVEST_CHOICES
    )

    pick_leader = ModelChoiceFilter(
        queryset=AuthUser.objects.filter(
            is_staff=True
        ),
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
