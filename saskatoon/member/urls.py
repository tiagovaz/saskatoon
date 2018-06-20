from django.conf.urls import url
from member import views

urlpatterns = [
    url(
        r'^(?P<pk>\d+)/profile/$',
        views.Profile.as_view(),
        name='profile'
    ),
]
