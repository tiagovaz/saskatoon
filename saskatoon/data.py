#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django_bootstrap_calendar
------------

Tests for `django_bootstrap_calendar` modules module.
"""

from django.utils import timezone
from django.conf import settings


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_calsqlite.sql',
    }
}

settings.configure(
    DEBUG=True,
    TEMPLATE_DEBUG=True,
    DATABASES=DATABASES,
    DEFAULT_DB_ALIAS='default',
)


from django_bootstrap_calendar.models import CalendarEvent

c = CalendarEvent(title="title test for the event", url="http://gnu.org", start=timezone.now, end=timezone.now)



print c