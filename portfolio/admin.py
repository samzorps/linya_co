from django.contrib import admin

from .models import *

admin.site.register([ImageCollection, Image, Contact, CodeProject])
