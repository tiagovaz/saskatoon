#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from forms import RFPForm, PropertyForm
from models import Actor, Person, Organization, Property, Address, Harvest, TreeType, Status, Equipment, EquipmentType, Country, State, City, Neighborhood, City, Neighborhood, EquipmentTypeAtProperty, \
    RequestForParticipation, Language
from user_profile.models import AuthUser


class AuthInline(admin.StackedInline):
    model = AuthUser
    fields = ('email','password',)
    max_num = 1
    can_delete = False

class PersonInline(admin.TabularInline):
    model = Harvest.pickers.through
    verbose_name = "Cueilleurs pour cette récolte"
    verbose_name_plural = "Cueilleurs pour cette récolte"
    form = RFPForm
    exclude = ['creation_date', 'confirmation_date']
    extra = 3

class HarvestAdmin(admin.ModelAdmin):
    inlines = (PersonInline,)

class PropertyInline(admin.TabularInline):
    model = Property
    extra = 0

class RequestForParticipationAdmin(admin.ModelAdmin):
    form = RFPForm

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
        
class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        PropertyInline,
    ]
    search_fields = ['name','description']

#class PersonAdmin(admin.ModelAdmin):

    # inlines = [
    #     AuthInline, PropertyInline,
    # ]

class EquipmentTypeAtPropertyInline(admin.TabularInline):
    model = EquipmentTypeAtProperty
    extra = 1
    
class PropertyAdmin(admin.ModelAdmin):
    model = Property
    form = PropertyForm
#   inlines = (EquipmentTypeAtPropertyInline,)
#   Use many checkboxes rather than a multiple selection box
#   formfield_overrides = {
#       models.ManyToManyField: {'widget': CheckboxSelectMultiple},
#   }



#class Neighborhood(admin.TabularInline):
#    model = Neighborhood

admin.site.register(Actor)
admin.site.register(Language)
admin.site.register(Person)
admin.site.register(Organization)
admin.site.register(Property,PropertyAdmin)
# admin.site.register(Property)
admin.site.register(Address)
admin.site.register(Harvest, HarvestAdmin)
admin.site.register(RequestForParticipation, RequestForParticipationAdmin)
admin.site.register(TreeType)
admin.site.register(Status)
admin.site.register(Equipment)
admin.site.register(EquipmentType)
admin.site.register(Neighborhood)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)
# TODO: comments
#admin.site.register(Comment)

#admin.site.register(AuthUser,AuthUserAdmin)
# unregister old user admin


