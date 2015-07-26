from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from models import Property,Address,Person,Organization,Actor,\
    TreeType,Status,Equipment,EquipmentType,EquipmentTypeAtProperty,Harvest,RequestForParticipation
    
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
    
class PropertyAdmin(admin.ModelAdmin):
    inlines = (EquipmentTypeAtPropertyInline,)
    # Use many checkboxes rather than a multiple selection box
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


admin.site.register(Actor)
admin.site.register(Person,PersonAdmin)
admin.site.register(Organization,OrganizationAdmin)
admin.site.register(Property,PropertyAdmin)
admin.site.register(Address)
admin.site.register(Harvest)
admin.site.register(RequestForParticipation)
admin.site.register(TreeType)
admin.site.register(Status)
admin.site.register(Equipment)
admin.site.register(EquipmentType)

#admin.site.register(AuthUser,AuthUserAdmin)
# unregister old user admin


