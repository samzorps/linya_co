from django.shortcuts import render, HttpResponse
from .models import ArtCollection, Contact, ArtPiece, Sizes, CodeProject

def home(request):
    context = {
        'mostRecentPiece': ArtPiece.objects.all().order_by(date_created)[0]
    }
    return render(request, home, context=context)
