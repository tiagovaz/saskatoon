from django.conf.urls import patterns, include, url
from django.contrib import admin
from saskatoon.views import Index, Profile, EquipmentForm, HarvestForm, Harvests, Calendar, DataTest, JsonCalendar, HarvestDetails, PersonAutocomplete

#admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'saskatoon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^user/(\w+)/$', Profile.as_view()),
    url(r'^cal/', Calendar.as_view()),
    url(r'^jsoncal/', JsonCalendar.as_view()),
    url(r'^test/', DataTest.as_view()),
    url(r'^harvests/$', Harvests.as_view()),
    url(r'^harvest/$', HarvestDetails.as_view()),
    url(r'^new_equipment/', EquipmentForm.as_view()),
    url(r'^harvests/new/', HarvestForm.as_view()),
    url(r'^$', Index.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^person-autocomplete/$', PersonAutocomplete.as_view(), name='person-autocomplete',),
    ]
