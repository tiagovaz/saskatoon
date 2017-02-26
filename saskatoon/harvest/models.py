# coding: utf-8
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse_lazy
import datetime
from harvest import signals

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

    image = models.ImageField(
        upload_to='fruits_images',
        verbose_name=_("Fruit image"),
        null=True
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
        help_text = _("Harvest in this property is authorized for the current season"),
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

    avg_nb_required_pickers = models.PositiveIntegerField(
        verbose_name=_("Required pickers on average"),
        null=True,
        default=1
    )

    public_access = models.BooleanField(
        verbose_name=_("Publicly accessible"),
        default=False,
    )

    neighbor_access = models.BooleanField(
        verbose_name=_("Access to neighboring terrain if needed"),
        default=False,
    )

    compost_bin = models.BooleanField(
        verbose_name=_("Compost bin closeby"),
        default=False,
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

    publishable_location = models.CharField(
        verbose_name=_("Publishable location"),
        help_text = _("Aproximative location, do not make public the real address."),
        max_length=50,
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

    changed_by = models.ForeignKey(
        'member.AuthUser',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("property")
        verbose_name_plural = _("properties")

    def __str__(self):
        if self.street_number:
            return u"%s at %s %s" % \
               (self.owner, self.street_number, self.street)
        else:
            return u"%s at %s" % \
               (self.owner, self.street)

    def short_address(self):
        if self.street_number and self.street and self.complement:
            return "%s %s, %s" % (self.street_number, self.street, self.complement)
        elif self.street and self.street_number:
            return "%s %s" % (self.street_number, self.street)
        elif self.street and self.complement:
            return "%s, %s" % (self.street, self.complement)
        else:
            return self.street

    def get_absolute_url(self):
        return reverse_lazy('harvest:property_detail', args=[self.id])

    def get_harvests(self):
        harvests_list = Harvest.objects.filter(property=self)
        return harvests_list

# SIGNALS CONNECTED
models.signals.pre_save.connect(
    signals.changed_by,
    sender=Property
)


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='properties_images',
    )

@python_2_unicode_compatible
class Harvest(models.Model):
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
        verbose_name=_("Fruit trees")
    )

    owner_present = models.BooleanField(
        verbose_name=_("Owner wants to be present"),
        default=False
    )

    owner_help = models.BooleanField(
        verbose_name=_("Owner wants to participate"),
        default=False
    )

    owner_fruit = models.BooleanField(
        verbose_name=_("Owner want his share of fruits"),
        default=False
    )

    pick_leader = models.ForeignKey(
        'member.AuthUser',
        null=True,
        blank=True,
        verbose_name="Pick leader"
    )

    start_date = models.DateTimeField(
        verbose_name=_("Start date"),
        blank=True,
        null=True
    )

    end_date = models.DateTimeField(
        verbose_name=_("End date"),
        blank=True,
        null=True
    )

    publication_date = models.DateTimeField(
        verbose_name=_("Publication date"),
        blank=True,
        null=True
    )

    equipment_reserved = models.ManyToManyField(
        'Equipment',
        verbose_name=_("Reserve equipment"),
        blank=True
    )

    creation_date = models.DateTimeField(
        verbose_name=_("Creation date"),
        auto_now=False,
        auto_now_add=True
    )

    nb_required_pickers = models.PositiveIntegerField(
        verbose_name=_("Number of required pickers"),
        default=3
    )

    about = models.TextField(
        verbose_name=_("Public announcement"),
        max_length=1000,
        help_text = _("If any help is needed from volunteer pickers, please describe them here."),
        null=True,
        blank=True
    )

    history = HistoricalRecords()

    changed_by = models.ForeignKey(
        'member.AuthUser',
        related_name='harvest_edited',
        null=True,
        blank=True
    )

    def get_status_l10n(self):
        status_list = list(HARVESTS_STATUS_CHOICES)
        for s in status_list:
            if s[0] in self.status:
                return s[1]

    def get_total_distribution(self):
        total = 0
        yields = HarvestYield.objects.filter(harvest=self)
        for y in yields:
            total += y.total_in_lb
        return total

    class Meta:
        verbose_name = _("harvest")
        verbose_name_plural = _("harvests")

    def __str__(self):
        if self.start_date:
            return u"Harvest on %s at %s" % (self.start_date,self.property)
        else:
            return u"Harvest at %s" % (self.property)

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


    def is_publishable(self):

        now = datetime.datetime.now()
        publication_hour = 18 #FIXME: add a model to set this up

        print("Publication date: ", self.publication_date)
        if self.publication_date != None:
            is_good_day = self.publication_date.day == now.day
            print(self.publication_date.day, now.day, "<== PUBLICATION DAY & NOW DAY")
            is_good_month = self.publication_date.month == now.month
            print(self.publication_date.month)
            is_good_year = self.publication_date.year == now.year
            print(self.publication_date.year)

            print(is_good_day, is_good_month, is_good_year)

            print("TODAY: ", now)
            if is_good_day and is_good_month and is_good_year:
                is_today = True
            else:
                is_today = False

            if self.status in ["Ready", "Date-scheduled", "Succeeded"]:
                if is_today == True:
                    print("is today")
                    if now.hour >= publication_hour and self.publication_date.hour < publication_hour+4: #FIXME: timezone
                        print("TODAY OK")
                        return True # publish if it was published today earlier and it's time to go online
                    else:
                        return False # do not publish otherwise
                else:
                    return True # publish if date of publication is in the pas
            else:
                return False # do not publish if harvest is not ready/scheduled/succeeded
        else:
            return False # do not publish if there's no publication_date

    def is_open_to_requests(self):
        now = datetime.datetime.now().date()
        start_date = self.start_date.date()
        if self.status in ["Ready", "Date-scheduled"] and self.is_publishable() and now <= start_date:
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse_lazy('harvest:harvest_detail', args=[self.id])

# SIGNALS CONNECTED
models.signals.pre_save.connect(
    signals.changed_by,
    sender=Harvest
)



class HarvestImage(models.Model):
    harvest = models.ForeignKey(
        Harvest,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='harvests_images',
    )

@python_2_unicode_compatible
class RequestForParticipation(models.Model):
    picker = models.ForeignKey(
        'member.Person',
        verbose_name=_("Requester")
    )

    number_of_people = models.PositiveIntegerField(
        verbose_name=_("How many people are you?"),
        default=1,
        validators=[
            MaxValueValidator(3),
            MinValueValidator(1)
        ]
    )

    comment = models.TextField(
        verbose_name=_("Comment"),
        null=True,
        blank=True
    )

    notes_from_pickleader = models.TextField(
        verbose_name=_("Notes from the pick leader."),
        null=True,
        blank=True
    )

    harvest = models.ForeignKey(
        'Harvest',
        verbose_name=_("Harvest"),
        related_name="request_for_participation"
    )

    creation_date = models.DateTimeField(
        verbose_name=_("Created on"),
        default=timezone.now
    )

    acceptation_date = models.DateTimeField(
        verbose_name=_("Accepted on"),
        null=True,
        blank=True
    )

    is_accepted = models.NullBooleanField(
        verbose_name=_("Accepted"),
        default=None,
        null = True,
        blank = True
    )

    showed_up = models.NullBooleanField(
        verbose_name=_("Showed up"),
        default=None,
        null = True,
        blank = True
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
        verbose_name=_("Weight (lb)"),
        validators=[
            MinValueValidator(0.0)
        ]
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
        related_name="equipment",
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

# SIGNALS CONNECTED
models.signals.post_save.connect(
    signals.comment_send_mail,
    sender=Comment
)
