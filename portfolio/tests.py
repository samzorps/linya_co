from django.test import TestCase
from .models import ArtCollection, Contact, ArtPiece, Sizes, CodeProject


# Create your tests here.
class TestCase1(TestCase):
    def setUp(self):
        ac1 = ArtCollection.objects.create(name='crayon',
                                     thumbnail='media/media_test/crayon_clipart.jpg',
                                     description='Linyas drawings in crayon. these\
                                     are priced at over nine million dollars each,\
                                     go fuck yourself if you offer anything less.')
        Sizes.objects.create(size='8x10', printing_price=15.00)
        ArtPiece.objects.create(name= 'django',
                                description= 'A scene from django by quintin tarentino.\
                                django looks away from blowing up house. ',
                                collection=ac1,
                                image='media/media_test/django.jpg',
                                is_for_sale=True,
                                base_price=50.00)
