from django.db import models
from django.utils import timezone
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class ArtCollection(models.Model):
    """A collection of images
    """
    name = models.CharField(max_length=100, unique=True)
    thumbnail = models.ImageField(upload_to='ArtCollectionThumbnails/')
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        """save a sizes object auto set its printing_price
        """
        if self.thumbnail.height != self.thumbnail.width:
            img = Image.open(self.thumbnail)
            side = min(img.size)
            img = ImageOps.fit(img, (side, side), method=3, bleed=0.0, centering=(0.5, 0.5))
            img = img.convert('RGB')
            output = BytesIO()
            img.save(output, format='JPEG')
            output.seek(0)
            # change the imagefield value to be the newley modifed image value
            self.thumbnail = InMemoryUploadedFile(output, 'ImageField',
                                                  f'{self.thumbnail.name.split(".")[0]}.jpg',
                                                  'image/jpeg', sys.getsizeof(output),
                                                  None)
        super().save(*args, **kwargs)


class Sizes(models.Model):
    """A print size
        - size stored as a string in the form "8x10"
        - printing_price will be overridden if it is able to be scraped from a
        printing website
    """
    class Meta:
        """metadata about Sizes class
        """
        verbose_name_plural = 'Sizes'
        verbose_name = 'Size'
    size = models.CharField(max_length=30)
    printing_price = models.DecimalField(max_digits=12, decimal_places=2)


class ArtPiece(models.Model):
    """A single art gallery image
    """
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    collection = models.ForeignKey('ArtCollection', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    image = models.ImageField(upload_to='ArtPieces/')
    is_for_sale = models.BooleanField(default=False)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    """This is the base price which will be used with a beautiful soup
        app scraping the kegprint price for the specific size
    """
    size_options = models.ManyToManyField('Sizes')
    def __str__(self):
        return self.name


class CodeProject(models.Model):
    """A single code project
    """
    name = models.CharField(max_length=100, unique=True)
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


    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)
        """
        TODO: email linya summary of new contact object
        """
