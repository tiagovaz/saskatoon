#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from forms import RFPForm, PropertyForm, HarvestForm, HarvestYieldForm
from member.models import *
from harvest.models import *
from harvest.forms import *


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 0


class PersonInline(admin.TabularInline):
    model = Harvest.pickers.through
    verbose_name = "Cueilleurs pour cette récolte"
    verbose_name_plural = "Cueilleurs pour cette récolte"
    form = RFPForm
    exclude = ['creation_date', 'confirmation_date']
    extra = 3


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        PropertyInline,
    ]
    search_fields = ['name', 'description']


class HarvestYieldInline(admin.TabularInline):
    model = HarvestYield
    form = HarvestYieldForm

class HarvestAdmin(admin.ModelAdmin):
    form = HarvestForm
    inlines = (PersonInline, HarvestYieldInline)


class RequestForParticipationAdmin(admin.ModelAdmin):
    form = RFPForm


class EquipmentTypeAtPropertyInline(admin.TabularInline):
    model = EquipmentTypeAtProperty
    extra = 1


class PropertyAdmin(admin.ModelAdmin):
    model = Property
    form = PropertyForm

admin.site.register(Property,PropertyAdmin)
admin.site.register(Harvest, HarvestAdmin)
admin.site.register(RequestForParticipation, RequestForParticipationAdmin)
admin.site.register(TreeType)
admin.site.register(HarvestStatus)
admin.site.register(Equipment)
admin.site.register(EquipmentType)
admin.site.register(HarvestYield)
admin.site.register(Comment)

admin.site.register(Actor)
admin.site.register(Language)
admin.site.register(Person)
admin.site.register(Organization)
admin.site.register(Address)
admin.site.register(Neighborhood)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)
