from django.conf.urls import patterns, url
from pages import views

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
)
