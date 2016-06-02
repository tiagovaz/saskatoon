from django.conf.urls import include, url
from django.contrib import admin
from harvest import views

urlpatterns = [
    url(r'^', include('pages.urls', namespace="pages")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^harvest/', include('harvest.urls', namespace="harvest")),
    url(r'^member/', include('member.urls', namespace="member")),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),
    url(r'^person-autocomplete/$', views.PersonAutocomplete.as_view(), name='person-autocomplete',),
    url(r'^actor-autocomplete/$', views.ActorAutocomplete.as_view(), name='actor-autocomplete',),
    url(r'^tree-autocomplete/$', views.TreeAutocomplete.as_view(), name='tree-autocomplete',),
    url(r'^property-autocomplete/$', views.PropertyAutocomplete.as_view(), name='property-autocomplete',),
    url(r'^equipment-autocomplete/$', views.EquipmentAutocomplete.as_view(), name='equipment-autocomplete',),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]