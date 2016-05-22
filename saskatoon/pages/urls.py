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
        r'^$',
        'django.contrib.auth.views.login',
        name='login'
    ),
)
