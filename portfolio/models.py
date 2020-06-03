from django.db import models
from django.utils import timezone
from bs4 import BeautifulSoup
import requests, lxml

def scrape_prices(size):
    if size == '8x10':
        size_slug = '8x10-art-prints'
    else:
        return False
    source = requests.get('https://www.printkeg.com/collections/fine-arts-printing/products/'
                          +size_slug).text
    soup = BeautifulSoup(source, 'lxml')
    price = soup.select("#price-preview")
    if price in [None, []]:
        return False
    price = price[0].text
    stripped_price = ''
    for char in price:
        if char in ".1234567890":
            stripped_price += char
    return float(stripped_price)


class ArtCollection(models.Model):
    """A collection of images
    """
    name = models.CharField(max_length=100, unique=True)
    thumbnail = models.ImageField(upload_to='ArtCollectionThumbnails/')
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    def __str__(self):
        return self.name


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

    def save(self, *args, **kwargs):
        """save a sizes object auto set its printing_price
        """
        super(Sizes, self).save(*args, **kwargs)
        pp = scrape_prices(self.size)
        if not pp:
            return
        self.printing_price = pp


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
