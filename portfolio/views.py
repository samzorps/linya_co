from django.shortcuts import render
from django.http import HttpResponse
from .models import ImageCollection, Image, CodeProject

# Create your views here.
def home(request):
    context = {
        'image_collections' : ImageCollection.objects.order_by('date_created'),
        'images' : Image.objects.order_by('date_created'),
        'code_projects' : CodeProject.objects.order_by('date_created'),
    }
    return render(request, 'index_template.html', context)
