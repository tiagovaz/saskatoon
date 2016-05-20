from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _
# FIXME: easymode to make database translatable
#from easymode.i18n.decorators import I18n

#from user_profile.models import AuthUser
#from django.contrib.auth.models import User

from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name = _("actor")
        verbose_name_plural = _("actors")

    def __str__(self):
        try:
            return self.person.__str__()
        except Person.DoesNotExist:
            # if it is not a person it must be an organization
            return self.organization.__str__()
        
@python_2_unicode_compatible
class Person(Actor):
    first_name = models.CharField(_("First name"),max_length=30)
    family_name = models.CharField(_("Family name"),max_length=50)
#    user = models.OneToOneField(User)
#    profile_image = models.ImageField(upload_to="uploads", blank=False, null=False, default="/static/images/defaultuserimage.png")
    phone = models.CharField(_("Phone"),max_length=30, null=True, blank=True)
    address = models.ForeignKey('saskatoon.Address', null=True, blank=True, verbose_name=_("Address"))
    comments = models.TextField(_("Comments"),blank=True)
    language = models.ForeignKey('saskatoon.Language', null=True, blank=True, verbose_name=_("Preferred language"))

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def __str__(self):
        return "%s %s" % (self.first_name,self.family_name)
    
    def name(self):
        return "%s %s" % (self.first_name,self.family_name)

@python_2_unicode_compatible
class Organization(Actor):
    civil_name = models.CharField(_("Name"),max_length=50)
    description = models.TextField(_("Description"),blank=True)
    address = models.ForeignKey('Address', null=True, verbose_name=_("Address"))
    contact = models.ForeignKey('Person', null=True, verbose_name=_("Contact person"))

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def __str__(self):
        return self.civil_name

    def name(self):
        return self.civil_name

#@I18n('name')
@python_2_unicode_compatible
class Neighborhood(models.Model):
    name = models.CharField(_("Name"),max_length=150)

    class Meta:
        verbose_name = _("neighborhood")
        verbose_name_plural = _("neighborhoods")

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class City(models.Model):
    name = models.CharField(_("Name"),max_length=150)

    class Meta:
        verbose_name=_("city")
        verbose_name_plural = _("cities")

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class State(models.Model):
    name = models.CharField(_("Name"),max_length=150)

    class Meta:
        verbose_name = _("state")
        verbose_name = _("states")

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Country(models.Model):
    name = models.CharField(_("Name"),max_length=150)

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Language(models.Model):
    name = models.CharField(_("Name"),max_length=150)

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class HarvestStatus(models.Model):
    short_name = models.CharField(_("Short name"),max_length=30)
    description = models.CharField(_("Description"),max_length=150)

    class Meta:
        verbose_name = _("harvest status")
        verbose_name_plural = _("harvest statuses")

    def __str__(self):
        return self.short_name


@python_2_unicode_compatible
class Address(models.Model):
    """Address for organization, persons and properties"""
    number = models.CharField(_("Number"),max_length=10)
    street = models.CharField(_("Street"),max_length=50)
    complement = models.CharField(_("Complement"),max_length=150, blank=True)
    neighborhood = models.ForeignKey('Neighborhood', verbose_name=_("Neighborhood"))
    city = models.ForeignKey('City', verbose_name=_("City"), default=1)
    state = models.ForeignKey('State', verbose_name=_("State"), default=1)
    country = models.ForeignKey('Country', verbose_name=_("Country"), default=1)
    longitude = models.FloatField(_("Longitude"),null=True, blank=True)
    latitude = models.FloatField(_("Latitude"),null=True, blank=True)

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self):
        return "%s %s, %s" % (self.number,self.street,self.city)

#@I18n('name','fruit_name')
@python_2_unicode_compatible
class TreeType(models.Model):
    name = models.CharField(_("Name"),max_length=20,default='')
    fruit_name = models.CharField(_("Fruit name"),max_length=20)
    season_start = models.DateField(_("Season start date"),blank=True,null=True)

    class Meta:
        verbose_name = _("tree type")
        verbose_name_plural = _("tree types")

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class EquipmentType(models.Model):
    name = models.CharField(_("Name"),max_length=50)

    class Meta:
        verbose_name = _("equipment type")
        verbose_name_plural = _("equipment types")

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Property(models.Model):
    """Property where you find one or more trees for harvesting."""
    is_active = models.BooleanField(_("Is active"),default='True')
    address = models.ForeignKey('Address',verbose_name=_("Address"))
    owner = models.ForeignKey('Actor',verbose_name=_("Owner"))
    equipment = models.ManyToManyField(EquipmentType,through='EquipmentTypeAtProperty',verbose_name=_("Equipment"))
    trees = models.ManyToManyField(TreeType,verbose_name=_("Fruit trees"))
    trees_location = models.CharField(_("Trees location"),null=True, blank=True, max_length=200)
    avg_nb_required_pickers = models.IntegerField(_("Required pickers on average"),default=1)
    public_access = models.BooleanField(_("Publicly accessible"),default='False')
    neighbor_access = models.BooleanField(_("Access to neighboring terrain if needed"),default='False')
    compost_bin = models.BooleanField(_("Compost bin closeby"),default='False')
    about = models.CharField(_("About"),max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = _("property")
        verbose_name_plural = _("properties")

    def __str__(self):
        return "Property of %s at %s %s" % (self.owner,self.address.number,self.address.street)

@python_2_unicode_compatible
class EquipmentTypeAtProperty(models.Model):
    equipment_type = models.ForeignKey(EquipmentType,verbose_name=_("Equipment type"))
    property = models.ForeignKey(Property,verbose_name=_("Property"))
    quantity = models.IntegerField(_("Quantity"),default=1)
    shared = models.BooleanField(_("Can be used outside of property"),default='False')
    
    class Meta:
        unique_together = ('equipment_type', 'property',)
    class Meta:
        verbose_name = _("equipment type at property")
        verbose_name_plural = _("equipment types at property")


    def __str__(self):
        return "%s %s at " % (self.quantity,self.equipment_type,self.property)

@python_2_unicode_compatible
class Harvest(models.Model):
#    """ Determines if this harvest appears on public calendar. """
    is_active = models.BooleanField(_("Is active"),default='True')
    status = models.ForeignKey('HarvestStatus', null=True,verbose_name=_("Harvest status"))
    property = models.ForeignKey('Property', null=True,verbose_name=_("Property"))
    trees = models.ManyToManyField('TreeType',verbose_name=_("Trees"))
    pick_leader = models.ForeignKey('Person', null=True, verbose_name="Pick leader")
    start_date = models.DateTimeField(_("Start"),blank=True, null=True)
    end_date = models.DateTimeField(_("End"),blank=True, null=True)
    nb_required_pickers = models.IntegerField(_("Number of required pickers"),default=3)
    pickers = models.ManyToManyField('Person', related_name='harvests', through='RequestForParticipation', verbose_name=_("Pickers' names"))
    equipment_reserved = models.ManyToManyField('Equipment',verbose_name=_("Reserve equipment"))
    owner_present = models.BooleanField(_("Owner wants to be present"),default='True')
    owner_help = models.BooleanField(_("Owner wants to participate"),default='False')
    owner_fruit = models.BooleanField(_("Owner wants his share of fruits"),default='True')
    about = models.TextField(_("About"),max_length=1000, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("harvest")
        verbose_name_plural = _("harvests")

    def __str__(self):
        return "Harvest on %s at %s" % (self.start_date,self.property)

@python_2_unicode_compatible
class RequestForParticipation(models.Model):
    picker = models.ForeignKey(Person,verbose_name=_("Picker"))
    harvest = models.ForeignKey(Harvest,verbose_name=_("Harvest"))
    first_time_picker = models.BooleanField(_("Is this your first pick with us?"),default = False)
    helper_picker = models.BooleanField(_("Can you help with equipment transportation?"),default = False)
    creation_date = models.DateTimeField(_("Created on"),default=timezone.now)
    confirmed = models.BooleanField(_("Confirmed"),default = False)
    confirmation_date = models.DateTimeField(_("Confirmed on"),default=timezone.now) #FIXME: can't be null... why?
    showed_up = models.BooleanField(_("Showed up"),default = True)
    is_cancelled = models.BooleanField(_("Canceled"),default=False)

    class Meta:
        verbose_name = _("request for participation")
        verbose_name_plural = _("requests for participation")

    def __str__(self):
        return "Request by %s to participate to %s" % (self.picker,self.harvest)

@python_2_unicode_compatible
class HarvestYield(models.Model):
    harvest = models.ForeignKey('Harvest',verbose_name=_("Harvest"))
    tree = models.ForeignKey('TreeType',verbose_name=_("Tree"))
    total_in_lb = models.FloatField(_("Total yield (lb)"))
    recipient = models.ForeignKey('Actor',verbose_name=_("Recipient"))

    class Meta:
        verbose_name = _("harvest yield")
        verbose_name_plural = _("harvest yields")

    def __str__(self):
        return "%.2f kg of %s to %s" % (self.total_in_lb,self.tree.fruit_name,self.recipient)
    
@python_2_unicode_compatible
class Equipment(models.Model):
    type = models.ForeignKey('EquipmentType',verbose_name=_("Type"))
    description = models.CharField(_("Description"),max_length=50)

    class Meta:
        verbose_name = _("equipment")
        verbose_name_plural = _("equipment")

    def __str__(self):
        return self.description
