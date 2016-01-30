from django.db import models
from django.utils import timezone
#from user_profile.models import AuthUser
#from django.contrib.auth.models import User

from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    def __str__(self):
        try:
            return self.person.__str__()
        except Person.DoesNotExist:
            # if it is not a person it must be an organization
            return self.organization.__str__()
        
@python_2_unicode_compatible
class Person(Actor):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)

#    user = models.OneToOneField(User)
#    profile_image = models.ImageField(upload_to="uploads", blank=False, null=False, default="/static/images/defaultuserimage.png")
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.ForeignKey('saskatoon.Address', null=True, blank=True)

    class Meta:
        verbose_name_plural = "People"

    def __str__(self):
        return "%s %s" % (self.first_name,self.last_name)
    
@python_2_unicode_compatible
class Organization(Actor):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    address = models.ForeignKey('Address', null=True)
    contact = models.ForeignKey('Person', null=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Neighborhood(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class City(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class State(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Country(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Address(models.Model):
    """Address for organization, persons and properties"""
    number = models.CharField(max_length=10)
    street = models.CharField(max_length=50)
    neighborhood = models.ForeignKey('Neighborhood')
    city = models.ForeignKey('City')
    state = models.ForeignKey('State')
    country = models.ForeignKey('Country')
    complement = models.CharField(max_length=150, blank=True)
    long = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "%s %s, %s" % (self.number,self.street,self.city)

@python_2_unicode_compatible
class TreeType(models.Model):
    name = models.CharField(max_length=20,default='')
    fruit_name = models.CharField(max_length=20)
    avg_harvest_date = models.DateField(blank=True,null=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class EquipmentType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Property(models.Model):
    """Property where you find one or more trees for harvesting."""
    address = models.ForeignKey('Address')
    owner = models.ForeignKey('Actor')
    equipment = models.ManyToManyField(EquipmentType,through='EquipmentTypeAtProperty')
    trees = models.ManyToManyField(TreeType)
    
    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return "Property of %s at %s %s" % (self.owner,self.address.number,self.address.street)

@python_2_unicode_compatible
class EquipmentTypeAtProperty(models.Model):
    equipment_type = models.ForeignKey(EquipmentType)
    property = models.ForeignKey(Property)
    number = models.IntegerField(default=1)    
    
    class Meta:
        unique_together = ('equipment_type', 'property',)

    def __str__(self):
        return "%s %s at " % (self.number,self.equipment_type,self.property)
        
@python_2_unicode_compatible
class Harvest(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    leader = models.ForeignKey('Person', null=True)
    scheduled_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    property = models.ForeignKey('Property', null=True)
    nb_required_pickers = models.IntegerField(default=3)
    pickers = models.ManyToManyField('Person', related_name='harvests', through='RequestForParticipation')
    equipment_reserved = models.ManyToManyField('Equipment')
    """ Determines if this harvest appears on public calendar. """
    published = models.BooleanField(default='False')
    status = models.ForeignKey('Status', null=True)
    
    def __str__(self):
        return "Harvest on %s at %s" % (self.scheduled_date,self.property)

@python_2_unicode_compatible
class RequestForParticipation(models.Model):
    picker = models.ForeignKey(Person)
    harvest = models.ForeignKey(Harvest)
    confirmed = models.BooleanField(default = False)
    showed_up = models.BooleanField(default = True)
    creation_date = models.DateTimeField(default=timezone.now)
    confirmation_date = models.DateTimeField(default=timezone.now) #FIXME: can't be null... why?
    is_cancelled = models.BooleanField(default=False)

    # FIXME: has to be removed for migration
    class Meta:
        auto_created = True
    
    def __str__(self):
        return "Request by %s to participate to %s" % (self.picker,self.harvest)

@python_2_unicode_compatible
class HarvestProduct(models.Model):    
    harvest = models.ForeignKey('Harvest')
    product = models.ForeignKey('TreeType')
    weight_in_kg = models.FloatField()

    def __str__(self):
        return "%s kg of %s harvested at %s" % (self.weight_in_kg,self.product.fruit_name,self.property)
    
@python_2_unicode_compatible
class Donation(models.Model):    
    harvest_product = models.ForeignKey('HarvestProduct')
    recipient = models.ForeignKey('Actor')
    weight_in_kg = models.FloatField()

    def __str__(self):
        return "%s kg of %s harvested at %s donated to %s" % (self.weight_in_kg,self.product.fruit_name,self.property,self.recipient)

    
@python_2_unicode_compatible
class Status(models.Model):
    """Status for Harvest."""
    # hardcoded status as requested
    # coding idea from http://www.b-list.org/weblog/2007/nov/02/handle-choices-right-way/
    RECONTACT = 0
    OBTAIN_CONTACT = 1
    WAITING_ON_OWNER = 2
    WAITING_ON_FRUIT = 3
    FRUIT_OWNER_READY = 4
    DONE = 5

    STATUS_CHOICES = (
    (RECONTACT, 'From last year: re-contact'),
    (OBTAIN_CONTACT, 'Obtain owner contact'),
    (WAITING_ON_OWNER, 'Waiting on owner'),
    (WAITING_ON_FRUIT, 'Waiting on fruit'),
    (FRUIT_OWNER_READY, 'Fruit and owner ready'),
    (DONE, 'Completed')
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=RECONTACT)

    class Meta:
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.STATUS_CHOICES[self.status][1]

    
@python_2_unicode_compatible
class Equipment(models.Model):
    type = models.ForeignKey('EquipmentType')
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Equipment"
        
