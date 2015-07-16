from django.conf.urls import patterns, include, url
from django.contrib import admin
from main.views import Index, Profile, EquipmentForm, HarvestForm, Harvests

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'saskatoon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^user/(\w+)/$', Profile.as_view()),
    url(r'^harvests/', Harvests.as_view()),
    url(r'^new_equipment/', EquipmentForm.as_view()),
    url(r'^new_harvest/', HarvestForm.as_view()),
    url(r'^$', Index.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
