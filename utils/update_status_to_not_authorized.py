# -*- coding: utf-8 -*-

import os, sys, django

sys.path.append("/var/www/saskatoon/saskatoon")
os.environ["DJANGO_SETTINGS_MODULE"] = "saskatoon.settings"
django.setup()


from harvest.models import *

properties = Property.objects.all()

for o in properties:
    o.authorized = None
    o.save()
