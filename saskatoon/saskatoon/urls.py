from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('pages.urls', namespace="pages")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^harvest/', include('harvest.urls', namespace="harvest")),
    url(r'^member/', include('member.urls', namespace="member")),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]