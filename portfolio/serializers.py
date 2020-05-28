from portfolio.models import Image, ImageCollection, CodeProject
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'name', 'date_created', 'description', 'collection', 'image']

class ImageCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageCollection
        fields = ['id', 'name', 'thumbnail', 'date_created', 'description']

class CodeProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeProject
        fields = ['id', 'name', 'thumbnail', 'date_created', 'description', 'live_version_link', 'gitHub_link']
