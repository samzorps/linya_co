from django.contrib import admin
from .models import ArtCollection, Contact, ArtPiece, Sizes, CodeProject

# Register your models here.
admin.site.register([ArtCollection, Contact, ArtPiece, Sizes, CodeProject])
