from django.db import models
from django.utils import timezone

class ImageCollection(models.Model):
    """A collection of images
    """
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField()
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    def __str__(self):
        return self.name

class Image(models.Model):
    """A single art gallery image
    """
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    collection = models.ForeignKey(ImageCollection, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    image = models.ImageField()

    def __str__(self):
        return self.name

class CodeProject(models.Model):
    """A single code project
    """
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField()
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    live_version_link = models.URLField(null=True, blank=True)
    gitHub_link = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name

class Contact(models.Model):
    """An instance of someone filling out the contact field
    """
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    time_sent = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
