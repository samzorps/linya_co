from django.contrib import admin

from .models import ImageCollection, Image, Contact, CodeProject

admin.site.register([ImageCollection, Image, Contact, CodeProject])
