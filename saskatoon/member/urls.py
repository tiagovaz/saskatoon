from django.conf.urls import url
from member import views

urlpatterns = [
    #TODO: profile view hasn't been implemented yet - do it or remove this
    url(r'^(?P<pk>\d+)/profile/$', views.Profile.as_view(), name='profile'),
    url(
        r'^people',
        views.PeopleList.as_view(),
        name='people'
    ),
]
