from django.shortcuts import render, HttpResponse
from .models import ArtCollection, Contact, ArtPiece, Sizes, CodeProject
from django.views.generic import ListView, DetailView

def home(request):
    context = {
        'mostRecentPiece': ArtPiece.objects.all().order_by(date_created)[0]
    }
    return render(request, home, context=context)


class CollectionListView(ListView):
    model = ArtCollection
#   template_name = <app>/<model>_<viewtype>.html
    context_object_name = 'collections'
    ordering = ['-date_created']

class CodeProjectListView(ListView):
    model = CodeProject

class CollectionDetailView(DetailView):
    model = ArtCollection

class ArtPiecetDetailView(DetailView):
    model = ArtPiece
