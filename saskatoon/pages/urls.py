from pages import views
from harvest.models import Property
from djgeojson.views import GeoJSONLayerView
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(
        r'^$',
        views.Index.as_view(),
        name='index'
    ),
    url(
        r'^login$',
        auth_views.login,
        name='login'
    ),
    url(
        r'^calendar$',
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

]
