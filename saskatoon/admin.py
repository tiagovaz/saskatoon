from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from models import Property,Address,Person,Organization,Actor,\
    TreeType,Status,Equipment,EquipmentType,EquipmentTypeAtProperty,Harvest,RequestForParticipation,Neighborhood, City, State, Country
from forms import *
from user_profile.models import AuthUser


    
class AuthInline(admin.StackedInline):
    model = AuthUser
    fields = ('email','password',)
    max_num = 1
    can_delete = False

class PropertyInline(admin.TabularInline):
    model = Property
    extra = 0

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
        
class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        PropertyInline,
    ]
    search_fields = ['name','description']

class PersonAdmin(admin.ModelAdmin):
    
    inlines = [
        AuthInline,PropertyInline,
    ]

class EquipmentTypeAtPropertyInline(admin.TabularInline):
    model = EquipmentTypeAtProperty
    extra = 1
    
#FIXME: not working
#class PropertyAdmin(admin.ModelAdmin):
#    inlines = (EquipmentTypeAtPropertyInline,)
#    # Use many checkboxes rather than a multiple selection box
#    formfield_overrides = {
#        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
#    }

#class Neighborhood(admin.TabularInline):
#    model = Neighborhood

admin.site.register(Actor)
admin.site.register(Person,PersonAdmin)
admin.site.register(Organization,OrganizationAdmin)
#admin.site.register(Property,PropertyAdmin)
admin.site.register(Property)
admin.site.register(Address)
class HarvestAdmin(admin.ModelAdmin):
    form = HarvestForm
admin.site.register(Harvest, HarvestAdmin)
admin.site.register(RequestForParticipation)
admin.site.register(TreeType)
admin.site.register(Status)
admin.site.register(Equipment)
admin.site.register(EquipmentType)
admin.site.register(Neighborhood)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)

#admin.site.register(AuthUser,AuthUserAdmin)
# unregister old user admin


