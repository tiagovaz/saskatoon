from django.db.models.query_utils import Q

from django.forms import CharField
from django.utils.translation import ugettext_lazy as _
import django_filters
from member.models import AuthUser, Neighborhood, Language
from harvest.models import Property


class PersonFilter(django_filters.FilterSet):




    person__neighborhood = django_filters.ModelChoiceFilter(
        queryset=Neighborhood.objects.all(),
        label=_("Neighborhood"),
        help_text="",
        required=False
    )

    person__language = django_filters.ModelChoiceFilter(
        queryset=Language.objects.all(),
        label=_("Language"),
        help_text="",
        required=False
    )

    person__first_name = django_filters.CharFilter(label="First name", method='custom_person_first_name_filter')
    person__family_name = django_filters.CharFilter(label="Family name", method='custom_person_family_name_filter')
    person__property = django_filters.BooleanFilter(label="Has property", method='custom_person_property_filter')


    def custom_person_first_name_filter(self, queryset, name, value):
        query = (Q(person__first_name__icontains=value))
        return queryset.filter(query)

    def custom_person_family_name_filter(self, queryset, name, value):
        query = (Q(person__family_name__icontains=value))
        return queryset.filter(query)

    def custom_person_property_filter(self, queryset, name, value):
        #TODO: fix this epic workaround
        if value is True:
            query = (Q(person__property__isnull=False))
        elif value is False:
            query = (Q(person__property__isnull=True))
        return queryset.filter(query)

    class Meta:
        model = AuthUser
        fields = [
        'person__neighborhood',
        'person__language',
        'person__first_name',
        'person__family_name',
        'person__property',
        ]