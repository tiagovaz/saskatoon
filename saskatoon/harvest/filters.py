import django_filters
from models import Harvest
from forms import HarvestFilterForm

class HarvestFilter(django_filters.FilterSet):
    class Meta:
        # FIXME: using model here will overpass the form, but we could not make the filter work with the form 
        model = Harvest
        form = HarvestFilterForm
        fields = ['status', 'pick_leader', 'is_active']
