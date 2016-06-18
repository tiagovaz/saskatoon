# coding: utf-8

from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse_lazy
import datetime


HARVESTS_STATUS_CHOICES = (
    (
        "To-be-confirmed",
        _("To be confirmed"),
    ),
    (
        "Orphan",
        _("Orphan"),
    ),
    (
        "Adopted",
        _("Adopted"),
    ),
    (
        "Date-scheduled",
        _("Date scheduled"),
    ),
    (
        "Ready",
        _("Ready"),
    ),
    (
        "Succeeded",
        _("Succeeded"),
    ),
    (
        "Cancelled",
        _("Cancelled"),
    )
)


@python_2_unicode_compatible
class TreeType(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=20,
        default=''
    )

    fruit_name = models.CharField(
        verbose_name=_("Fruit name"),
        max_length=20
    )

    season_start = models.DateField(
        verbose_name=_("Season start date"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("tree type")
        verbose_name_plural = _("tree types")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class EquipmentType(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=50
    )

    class Meta:
        verbose_name = _("equipment type")
        verbose_name_plural = _("equipment types")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Property(models.Model):
    """
    Property where you find one or more trees for harvesting.
    """
    is_active = models.BooleanField(
        verbose_name=_("Is active"),
        default='True'
    )

    owner = models.ForeignKey(
        'member.Actor',
        verbose_name=_("Owner")
    )

    trees = models.ManyToManyField(
        'TreeType',
        verbose_name=_("Fruit trees")
    )

    trees_location = models.CharField(
        verbose_name=_("Trees location"),
        null=True,
        blank=True,
        max_length=200
    )

    avg_nb_required_pickers = models.IntegerField(
        verbose_name=_("Required pickers on average"),
        default=1
    )

    public_access = models.BooleanField(
        verbose_name=_("Publicly accessible"),
        default='False'
    )

    neighbor_access = models.BooleanField(
        verbose_name=_("Access to neighboring terrain if needed"),
        default='False'
    )

    compost_bin = models.BooleanField(
        verbose_name=_("Compost bin closeby"),
        default='False'
    )

    street_number = models.CharField(
        verbose_name=_("Number"),
        max_length=10,
        null=True,
        blank=True
    )

    street = models.CharField(
        verbose_name=_("Street"),
        max_length=50,
        null=True,
        blank=True
    )

    complement = models.CharField(
        verbose_name=_("Complement"),
        max_length=150,
        null=True,
        blank=True
    )

    postal_code = models.CharField(
        verbose_name=_("Postal code"),
        max_length=10,
        null=True,
        blank=True
    )

    neighborhood = models.ForeignKey(
        'member.Neighborhood',
        verbose_name=_("Neighborhood"),
        null=True
    )

    city = models.ForeignKey(
        'member.City',
        verbose_name=_("City"),
        null=True,
        default=1
    )

    state = models.ForeignKey(
        'member.State',
        verbose_name=_("State"),
        null=True,
        default=1
    )

    country = models.ForeignKey(
        'member.Country',
        verbose_name=_("Country"),
        null=True,
        default=1
    )

    longitude = models.FloatField(
        verbose_name=_("Longitude"),
        null=True,
        blank=True
    )

    latitude = models.FloatField(
        verbose_name=_("Latitude"),
        null=True,
        blank=True
    )

    about = models.CharField(
        verbose_name=_("About"),
        max_length=1000,
        null=True,
        blank=True
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("property")
        verbose_name_plural = _("properties")

    def __str__(self):
        return u"Property of %s at %s %s" % \
               (self.owner, self.street_number, self.street)

    def get_absolute_url(self):
        return reverse_lazy('harvest:property_detail', args=[self.id])


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images')
    image = models.ImageField()


@python_2_unicode_compatible
class Harvest(models.Model):
    """
    Determines if this harvest appears on public calendar.
    """

    is_active = models.BooleanField(
        verbose_name=_("Is active"),
        default='True'
    )

    status = models.CharField(
        choices=HARVESTS_STATUS_CHOICES,
        max_length=100,
        null=True,
        verbose_name=_("Harvest status")
    )

    property = models.ForeignKey(
        'Property',
        null=True,
        verbose_name=_("Property")
    )

    trees = models.ManyToManyField(
        'TreeType',
        verbose_name=_("Trees")
    )

    pick_leader = models.ForeignKey(
        'member.AuthUser',
        null=True,
        blank=True,
        verbose_name="Pick leader"
    )

    start_date = models.DateTimeField(
        verbose_name=_("Start"),
        blank=True,
        null=True
    )

    end_date = models.DateTimeField(
        verbose_name=_("End"),
        blank=True,
        null=True
    )

    nb_required_pickers = models.IntegerField(
        verbose_name=_("Number of required pickers"),
        default=3
    )

    pickers = models.ManyToManyField(
        'member.Person',
        related_name='harvests',
        verbose_name=_("Pickers' names"),
        blank=True
    )

    equipment_reserved = models.ManyToManyField(
        'Equipment',
        verbose_name=_("Reserve equipment"),
        blank=True
    )

    owner_present = models.BooleanField(
        verbose_name=_("Owner wants to be present"),
        default='True'
    )

    owner_help = models.BooleanField(
        verbose_name=_("Owner wants to participate"),
        default='False'
    )

    owner_fruit = models.BooleanField(
        verbose_name=_("Owner wants his share of fruits"),
        default='True'
    )

    about = models.TextField(
        verbose_name=_("About"),
        max_length=1000,
        null=True,
        blank=True,
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("harvest")
        verbose_name_plural = _("harvests")

    def __str__(self):
        return "Harvest on %s at %s" % (self.start_date,self.property)

    def is_urgent(self):
        if self.start_date:
            day_before_harvest = (datetime.datetime.now() - self.start_date).days

            if not self.pick_leader and day_before_harvest < 14:
                return True
            elif self.status == 'Date-scheduled' and day_before_harvest < 3:
                return True

        return False

    def is_happening(self):
        if self.start_date:
            day_before_harvest = (datetime.datetime.now() - self.start_date).days

            if self.status == 'Ready' and day_before_harvest == 0:
                return True

        return False

    def get_absolute_url(self):
        return reverse_lazy('harvest:harvest_detail', args=[self.id])


@python_2_unicode_compatible
class RequestForParticipation(models.Model):
    picker = models.EmailField(
        verbose_name=_("Email of contact person")
    )

    phone = models.CharField(
        verbose_name=_("Phone of contact person"),
        max_length=10,
        null=True,
        blank=True
    )

    number_of_people = models.IntegerField(
        verbose_name=_("How many people are you?"),
        default=0,
    )

    harvest = models.ForeignKey(
        'Harvest',
        verbose_name=_("Harvest")
    )

    first_time_picker = models.BooleanField(
        verbose_name=_("Is this your first pick with us?"),
        default=False
    )

    helper_picker = models.BooleanField(
        verbose_name=_("Can you help with equipment transportation?"),
        default=False
    )

    creation_date = models.DateTimeField(
        verbose_name=_("Created on"),
        default=timezone.now
    )

    confirmed = models.BooleanField(
        verbose_name=_("Confirmed"),
        default=False
    )

    confirmation_date = models.DateTimeField(
        verbose_name=_("Confirmed on"),
        null=True,
        default=timezone.now,
    )

    showed_up = models.BooleanField(
        verbose_name=_("Showed up"),
        default=True
    )

    is_cancelled = models.BooleanField(
        verbose_name=_("Canceled"),
        default=False
    )

    class Meta:
        verbose_name = _("request for participation")
        verbose_name_plural = _("requests for participation")

    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = timezone.now()

        super(RequestForParticipation, self).save(*args, **kwargs)

    def __str__(self):
        return "Request by %s to participate to %s" % \
               (self.picker, self.harvest)


@python_2_unicode_compatible
class HarvestYield(models.Model):
    harvest = models.ForeignKey(
        'Harvest',
        verbose_name=_("Harvest")
    )

    tree = models.ForeignKey(
        'TreeType',
        verbose_name=_("Tree")
    )

    total_in_lb = models.FloatField(
        verbose_name=_("Total yield (lb)")
    )

    recipient = models.ForeignKey(
        'member.Actor',
        verbose_name=_("Recipient")
    )

    class Meta:
        verbose_name = _("harvest yield")
        verbose_name_plural = _("harvest yields")

    def __str__(self):
        return "%.2f kg of %s to %s" % \
               (self.total_in_lb, self.tree.fruit_name, self.recipient)


@python_2_unicode_compatible
class Equipment(models.Model):
    type = models.ForeignKey(
        'EquipmentType',
        verbose_name=_("Type")
    )

    description = models.CharField(
        verbose_name=_("Description"),
        max_length=50
    )

    owner = models.ForeignKey(
        'member.Actor',
        verbose_name=_("Owner"),
        null=True,
        blank=True
    )

    property = models.ForeignKey(
        'Property',
        verbose_name=_("Property"),
        null=True,
        blank=True
    )

    shared = models.BooleanField(
        verbose_name=_("Shared"),
        help_text=_("Can be used in harvests outside of property"),
        default='False'
    )

    class Meta:
        verbose_name = _("equipment")
        verbose_name_plural = _("equipment")

    def __str__(self):
        return "%s (%s)" % (self.description,self.type)


@python_2_unicode_compatible
class Comment(models.Model):
    content = models.CharField(
        verbose_name=_("Content"),
        max_length=500
    )

    created_date = models.DateTimeField(
        verbose_name=_("Created date"),
        auto_now_add=True
    )

    author = models.ForeignKey(
        'member.AuthUser',
        verbose_name=_("Author"),
        related_name="Comment"
    )

    harvest = models.ForeignKey(
        'Harvest',
        verbose_name=_("harvest"),
        related_name="comment"
    )

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return self.content
