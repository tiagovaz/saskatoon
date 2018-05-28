from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    url(r'^$', views.index, name='index'),

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

]
