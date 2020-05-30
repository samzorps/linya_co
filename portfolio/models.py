from django.db import models
from django.utils import timezone

class ArtCollection(models.Model):
    """A collection of images
    """
    name = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='ArtCollectionThumbnails/')
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    def __str__(self):
        return self.name

class Sizes(models.Model):
    class Meta:
        """metadata about Sizes class
        """
        verbose_name_plural = 'Sizes'
        verbose_name = 'Size'
    size = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=12, decimal_places=2)


class ArtPiece(models.Model):
    """A single art gallery image
    """

    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    collection = models.ForeignKey('ArtCollection', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    image = models.ImageField(upload_to='ArtPieces/')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    size_options = models.ManyToManyField('Sizes')
    def __str__(self):
        return self.name

class CodeProject(models.Model):
    """A single code project
    """
    name = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='codeProjectThumbnails/')
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
