import django_filters
from models import Harvest

class HarvestFilter(django_filters.FilterSet):
    class Meta:
        model = Harvest
        fields = ['status', 'pick_leader']
