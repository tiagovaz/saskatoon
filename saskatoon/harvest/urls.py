from django.conf.urls import url, include
from harvest import views
from django.views.decorators.cache import cache_page
from django.core.cache import cache

urlpatterns = [
    url(
        r'^organizations/$',
        #cache_page(60 * 60 * 24, key_prefix="organization")(views.OrganizationList.as_view()),
        views.OrganizationList.as_view(),
        name='organization_list'
    ),
    url(
        r'^organizations/active/$',
        views.PropertyList.as_view(),
        name='organization_list_active'
    ),
    url(
        r'^organization/(?P<pk>\d+)$',
        views.PropertyDetail.as_view(),
        name='organization_detail'
    ),
    url(
        r'^organizations/create$',
        views.PropertyCreate.as_view(),
        name='organization_create'
    ),
    url(
        r'^organizations/(?P<pk>\d+)/update$',
        views.PropertyUpdate.as_view(),
        name='organization_update'
    ),
    url(
        r'^properties/$',
        #cache_page(60 * 60 * 24, key_prefix='property')(views.PropertyList.as_view()),
        views.PropertyList.as_view(),
        name='property_list'
    ),
    url(
        r'^properties/active/$',
        views.PropertyList.as_view(),
        name='property_list_active'
    ),
    url(
        r'^property/(?P<pk>\d+)$',
        views.PropertyDetail.as_view(),
        name='property_detail'
    ),
    url(
        r'^properties/create$',
        views.PropertyCreate.as_view(),
        name='property_create'
    ),
    url(
        r'^properties/create_pending$',
        views.PublicPropertyCreate.as_view(),
        name='property_create_pending'
    ),
    url(
        r'^properties/thanks$',
        views.PropertyThanks.as_view(),
        name='property_thanks'
    ),
    url(
        r'^properties/(?P<pk>\d+)/update$',
        views.PropertyUpdate.as_view(),
        name='property_update'
    ),
    url(
        r'^properties/(?P<pk>\d+)/new_image$',
        views.PropertyImageCreate.as_view(),
        name='property_add_image'
    ),
    url(
        r'^properties/(?P<property>\d+)/add_equipment$',
        views.EquipmentCreate.as_view(),
        name='property_add_equipment'
    ),
    url(
        r'^list/$',
#        cache_page(60 * 60 * 24, key_prefix='harvest')(views.HarvestList.as_view()),
        views.HarvestList.as_view(),
        name='harvest_list'
    ),
    url(
        r'^(?P<pk>\d+)$',
        views.HarvestDetail.as_view(),
        name='harvest_detail'
    ),
    url(
        r'^(?P<pk>\d+)/add_recipient$',
        views.HarvestYieldCreate.as_view(),
        name='harvest_add_recipient'
    ),
    url(
        r'^(?P<pk>\d+)/edit_recipient$',
        views.HarvestYieldUpdate.as_view(),
        name='harvest_edit_recipient'
    ),
    url(
        r'^create$',
        views.HarvestCreate.as_view(),
        name='harvest_create'
    ),
    url(
        r'^create/(?P<property>\d+)$',
        views.HarvestCreate.as_view(),
        name='harvest_create'
    ),
    url(
        r'^(?P<pk>\d+)/update$',
        views.HarvestUpdate.as_view(),
        name='harvest_update'
    ),
    url(
        r'^(?P<pk>\d+)/adopt$',
        views.HarvestAdopt.as_view(),
        name='harvest_adopt'
    ),
    url(
        r'^participations/(?P<pk>\d+)/update$',
        views.RequestForParticipationUpdate.as_view(),
        name='participation_update'
    ),
    url(
        r'^participations/list/$',
        views.ParticipationList.as_view(),
        name='participation_list'
    ),
    url(
        r'^equipments/list/$',
        cache_page(60 * 60 * 24, key_prefix='equipment')(views.EquipmentList.as_view()),
        name='equipment_list'
    ),
    url(
        r'^equipments/create$',
        views.EquipmentCreate.as_view(),
        name='equipment_create'
    ),
    url(
        r'^(?P<pk>\d+)/new_participation$',
        views.RequestForParticipationCreate.as_view(),
        name='participation_create'
    ),
    url(
        r'^(?P<pk>\d+)/new_comment$',
        views.CommentCreate.as_view(),
        name='comment_create'
    ),
    url(
        r'^stats/(?P<season>\w+)/$',
        views.Stats.as_view(),
        name='stats'
    ),
    url(r'^select2/', include('django_select2.urls')),

]
