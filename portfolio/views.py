from django.shortcuts import render, HttpResponse
from .models import ArtCollection, Contact, ArtPiece, Sizes, CodeProject
from django.views.generic import ListView, DetailView

def home(request):
    context = {
        'mostRecentArtPiece': ArtPiece.objects.latest('date_created'),
        'mostRecentCodeProject': CodeProject.objects.latest('date_created'),
    }
    return render(request, 'portfolio/home.html', context=context)

def store(request):
    context = {
        'piecesForSale': ArtPiece.objects.filter(is_for_sale=True),
    }
    return render(request, 'portfolio/store.html', context=context)

def aboutMe(request):
    return render(request, 'portfolio/about_me.html')

class ArtPieceDetailView(DetailView):
    model = ArtPiece
    context_object_name = 'art_piece'

class ArtCollectionDetailView(DetailView):
    model = ArtCollection
    context_object_name = 'collection'

class CodeProjectDetailView(DetailView):
    model = CodeProject

class ArtCollectionListView(ListView):
    model = ArtCollection
    template_name = 'portfolio/artcollection_list.html'
    context_object_name = 'collections'
    ordering = ['-date_created']
    paginate_by = 3

class ArtPieceListView(ListView):
    model = ArtPiece
    paginate_by = 8

class CodeProjectListView(ListView):
    model = CodeProject
    paginate_by = 8
