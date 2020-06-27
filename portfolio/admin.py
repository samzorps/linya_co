from django.contrib import admin
from .models import ArtCollection, ArtPiece, Sizes, CodeProject

# Register your models here.
admin.site.register([Sizes])

@admin.register(ArtPiece)
class ArtPieceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name",]}

@admin.register(ArtCollection)
class ArtCollectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name",]}

@admin.register(CodeProject)
class CodeProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name",]}
