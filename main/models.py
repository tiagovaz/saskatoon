from django.db import models
from django.utils import timezone
from user_profile.models import AuthUser

class Owner(AuthUser):
    pass

class PickLeader(AuthUser):
    pass

class Picker(AuthUser):
    pass

class Property(models.Model):
    """Property where you find one or more trees for harvesting."""
    updated = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    address = models.ForeignKey('Address', null=True)
    owner = models.ForeignKey('Owner', null=True)
    n_laders = models.IntegerField(default=0)
    picture = models.FileField()

    def __unicode__(self):
        return self.address.street

class Institution(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.ForeignKey('Address', null=True)
    contact = models.ForeignKey('user_profile.AuthUser', null=True)

    # Set if it's the harverster org...
    is_organizer = models.BooleanField(default=False)

    # ...so override the save method
    def save(self, *args, **kwargs):
        if self.is_organizer:
            try:
                temp = Institution.objects.get(is_organizer=True)
                if self != temp:
                    temp.is_organizer = False
                    temp.save()
            except Institution.DoesNotExist:
                pass
        super(Institution, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Address(models.Model):
    """Address for users, properties or recipients"""
    updated = models.DateTimeField(default=timezone.now)
    street = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    area_code = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    complement = models.CharField(max_length=150)
    long = models.FloatField(null=True, blank=True, default=None)
    lat = models.FloatField(null=True, blank=True, default=None)

    def __unicode__(self):
        return self.number + ' ' + self.street

class TreeType(models.Model):
    fruit_name = models.CharField(max_length=200)
    avg_harvest_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.fruit_name

class Harvest(models.Model):
    description = models.CharField(max_length=200)
    updated = models.DateTimeField(default=timezone.now)
    leader = models.ForeignKey('PickLeader', related_name="pickleader", null=True)
    status = models.ForeignKey('Status', null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    property = models.ForeignKey('Property', null=True)
    recipient = models.ManyToManyField('Recipient', null=True)
    n_required_pickers = models.IntegerField(default=3)
    pickers = models.ManyToManyField('Picker', null=True)

    def __unicode__(self):
        return self.description

class Status(models.Model):
    """Status for Harvest."""
    # hardcoded status as requested
    # coding idea from http://www.b-list.org/weblog/2007/nov/02/handle-choices-right-way/
    RECONTACT = 0
    OBTAIN_CONTACT = 1
    WAITING_ON_OWNER = 2
    WAITING_ON_FRUIT = 3
    FRUIT_OWNER_READY = 4
    SCHEDULED = 5
    FULL = 6
    SUCCEEDED = 7
    CANCELLED = 8

    STATUS_CHOICES = (
    (RECONTACT, 'From last year: re-contact'),
    (OBTAIN_CONTACT, 'Obtain owner contact'),
    (WAITING_ON_OWNER, 'Waiting on owner'),
    (WAITING_ON_FRUIT, 'Waiting on fruit'),
    (FRUIT_OWNER_READY, 'Fruit and owner ready'),
    (SCHEDULED, 'Scheduled in calendar'),
    (FULL, 'Full'),
    (SUCCEEDED, 'Succeeded'),
    (CANCELLED, 'Cancelled')
    )

    updated = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(choices=STATUS_CHOICES, default=RECONTACT, unique=True)

    def __unicode__(self):
        return self.STATUS_CHOICES[self.status][1]

class Comment(models.Model):
    """Comment for Harvest."""
    commenter = models.ForeignKey('user_profile.AuthUser', null=True)
    harvest = models.ForeignKey('Harvest', null=True)

class Recipient(models.Model):
    updated = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    quantity = models.IntegerField()

    def __unicode__(self):
        return self.name