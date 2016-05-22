from django.conf.urls import patterns, url
from member import views

urlpatterns = patterns(
    '',
    url(
        r'^profile/(?P<pk>\d+)$',
        views.Profile.as_view(),
        name='profile'
    ),

)
