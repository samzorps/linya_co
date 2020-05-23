from django.db import models
from django.utils import timezone

class Collection(models.Model):
    """A collection of images
    """
    id = models.IntegerField()
    image = models.ImageField()
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()


class Image(models.Model):
    """A single portfolio image
    """
    id = models.IntegerField()
    name = models.CharField()
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True)

class Contact(models.Model):
    """An instance of someone filling out the contact field
    """
    id = models.IntegerField()
    name = models.CharField()
    email = models.EmailField()
    message = models.TextField()
    time_sent = models.DateTimeField(auto_now_add=True)
