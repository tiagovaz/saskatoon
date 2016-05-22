import suit.widgets
from django import forms
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from django.db import models

FORMFIELD_FOR_DBFIELD_DEFAULTS.update({
    models.DateTimeField: {
        'form_class': forms.SplitDateTimeField,
        'widget': suit.widgets.SuitSplitDateTimeWidget
    },
    models.DateField: {'widget': suit.widgets.SuitDateWidget},
    models.TimeField: {'widget': suit.widgets.SuitTimeWidget},
})