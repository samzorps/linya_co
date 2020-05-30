from django.test import TestCase
from .models import ArtCollection, Contact, ArtPiece, Sizes, CodeProject


# Create your tests here.
class ArtCollectionTestCase(TestCase):
    def setUp(self):
        ArtCollection.objects.create(name='crayon',
                                     thumbnail='media/media_test/crayon_clipart.jpg',\
                                     description='Linyas drawings in crayon. these\
                                     are priced at over nine million dollars each, \
                                     go fuck yourself if you offer anything less.')
