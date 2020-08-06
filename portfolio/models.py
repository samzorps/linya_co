import sys
import math
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageOps
from io import BytesIO


class ArtCollection(models.Model):
    """A collection of images
    """
    name = models.CharField(max_length=100, unique=True)
    thumbnail = models.ImageField(upload_to='ArtCollectionThumbnails/')
    date_created = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=50)
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
            img.close()
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
    size = models.CharField(max_length=30, primary_key=True)
    printing_price = models.DecimalField(max_digits=12, decimal_places=2)


class ArtPiece(models.Model):
    """A single art gallery image
    """
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    collection = models.ForeignKey('ArtCollection', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    image = models.ImageField(upload_to='ArtPieces/', default='media/placeholder_image.jpg')
    image_cut_square = models.ImageField(upload_to="ArtPieces/", default='media/placeholder_image.jpg')
    secondary_image = models.ImageField(upload_to='ArtPieces/', null=True, blank=True)
    is_for_sale = models.BooleanField(default=False)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    slug = models.SlugField(max_length=50)
    """This is the base price which will be used with
    the printing price for the size to get the final sale price
    """
    size_options = models.ManyToManyField('Sizes')
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        """save a ArtPiece object auto set its image_cut_square and image
        """
        # cut image_cut_square into a square
        if self.image_cut_square.height != self.image_cut_square.width:
            img_cs = Image.open(self.image_cut_square)
            side = min(img_cs.size)
            img_cs = ImageOps.fit(img_cs, (side, side), method=3, bleed=0.0, centering=(0.5, 0.5))
            img_cs = img_cs.convert('RGB')
            output = BytesIO()
            img_cs.save(output, format='JPEG')
            output.seek(0)
            # change the imagefield value to be the newley modifed image value
            self.image_cut_square = InMemoryUploadedFile(output, 'ImageField',
                                                         f'{self.image_cut_square.name.split(".")[0]}.jpg',
                                                         'image/jpeg', sys.getsizeof(output),
                                                         None)
            img_cs.close()

        # create a white square and paste 'image' inside to get a square version
        if self.image.height != self.image.width:
            img_ws = Image.open(self.image)
            side = max(img_ws.size)
            img_ws = img_ws.convert('RGB')
            white_img = Image.new('RGB', (side, side), color='white')
            paste_location = int(math.floor(((max(img_ws.size)-min(img_ws.size))/2)))
            if img_ws.size[0] > img_ws.size[1]:
                white_img.paste(img_ws, (0, paste_location))
            else:
                white_img.paste(img_ws, (paste_location, 0))
            output = BytesIO()
            white_img.save(output, format='JPEG')
            output.seek(0)
            # change the imagefield value to be the newley modifed image value
            self.image = InMemoryUploadedFile(output, 'ImageField',
                                              f'{self.image.name.split(".")[0]}.jpg',
                                              'image/jpeg', sys.getsizeof(output),
                                              None)
            img_ws.close()
            white_img.close()

        super().save(*args, **kwargs)


class CodeProject(models.Model):
    """A single code project
    """
    name = models.CharField(max_length=100, unique=True)
    thumbnail = models.ImageField(upload_to='codeProjectThumbnails/')
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    live_version_link = models.URLField(null=True, blank=True)
    gitHub_link = models.URLField(null=True, blank=True)
    slug = models.SlugField(max_length=50)
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
            img.close()
        super().save(*args, **kwargs)
