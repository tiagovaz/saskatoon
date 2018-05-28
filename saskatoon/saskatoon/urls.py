"""gentella URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from harvest import views
from django.views.static import serve
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # app/ -> Gentelella UI and resources
    url(r'^', include('app.urls', namespace='app')),

    # member/
    url(r'^member/', include('member.urls', namespace="member")),

    # harvest/
    url(r'^harvest/', include('harvest.urls', namespace="harvest")),

    # From saskatoon app
    url(
        r'^logout/$',
        auth_views.logout,
        {'next_page': '/'},
        name="logout"
    ),
    url(
        r'^i18n/',
        include('django.conf.urls.i18n')
    ),
    url(
        r'^person-autocomplete/$',
        views.PersonAutocomplete.as_view(),
        name='person-autocomplete'
    ),
    url(
        r'^pickleader-autocomplete/$',
        views.PickLeaderAutocomplete.as_view(),
        name='pickleader-autocomplete'
    ),
    url(
        r'^actor-autocomplete/$',
        views.ActorAutocomplete.as_view(),
        name='actor-autocomplete'
    ),
    url(
        r'^tree-autocomplete/$',
        views.TreeAutocomplete.as_view(),
        name='tree-autocomplete'
    ),
    url(
        r'^property-autocomplete/$',
        views.PropertyAutocomplete.as_view(),
        name='property-autocomplete'
    ),
    url(
        r'^equipment-autocomplete/$',
        views.EquipmentAutocomplete.as_view(),
        name='equipment-autocomplete'
    ),
    url(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT}
    ),
]
