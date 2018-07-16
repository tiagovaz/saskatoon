from django.conf.urls import url
from member import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    #TODO: profile view hasn't been implemented yet - do it or remove this
    url(r'^(?P<pk>\d+)/profile/$', views.Profile.as_view(), name='profile'),
    url(
        r'^people',
        cache_page(60 * 60 * 24, key_prefix="people")(views.PeopleList.as_view()),
        name='people'
    ),
]
