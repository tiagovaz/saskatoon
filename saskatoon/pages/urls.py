from django.conf.urls import patterns, url
from pages import views
from harvest.models import Property
from djgeojson.views import GeoJSONLayerView


urlpatterns = patterns(
    '',
    url(
        r'^index/$',
        views.Index.as_view(),
        name='index'
    ),
    url(
        r'^login$',
        'django.contrib.auth.views.login',
        name='login'
    ),
    url(
        r'^$',
        views.Calendar.as_view(),
        name='calendar'
    ),
    url(
        r'^jsoncal',
        views.JsonCalendar.as_view(),
        name='calendarJSON'
    ),
    url(r'^data.geojson$',
        GeoJSONLayerView.as_view(model=Property, properties=('id', 'get_owner_name', 'short_address')),
        name='data')

)
