from django.http import JsonResponse#, response, HttpResponse
from django.views.decorators.csrf import csrf_exempt
#from rest_framework.parsers import JSONParser
from portfolio.models import Image, ImageCollection, CodeProject
from portfolio.serializers import ImageSerializer, ImageCollectionSerializer, CodeProjectSerializer

@csrf_exempt
def image_list(request):
    """
    List all images
    """
    if request.method == 'GET':
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def image_collection_list(request):
    """
    List all image collections
    """
    if request.method == 'GET':
        image_collections = ImageCollection.objects.all()
        serializer = ImageCollectionSerializer(image_collections, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def code_project_list(request):
    """
    List all code projects
    """
    if request.method == 'GET':
        code_projects = CodeProject.objects.all()
        serializer = CodeProjectSerializer(code_projects, many=True)
        return JsonResponse(serializer.data, safe=False)
