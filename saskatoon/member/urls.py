from django.conf.urls import patterns, url
from member import views

urlpatterns = patterns(
    '',
    url(
        r'^(?P<pk>\d+)/profile/$',
        views.Profile.as_view(),
        name='profile'
    ),
)
