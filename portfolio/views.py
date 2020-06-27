from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail, BadHeaderError
from .models import ArtCollection, ArtPiece, Sizes, CodeProject
from .forms import ContactForm


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

def contactMe(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['linya.a.hu@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "contactme.html", {'form': form})

def success(request):
    return HttpResponse('Success! Thank you for your message.')

class ArtPieceDetailView(DetailView):
    model = ArtPiece
    context_object_name = 'art_piece'

class ArtCollectionDetailView(DetailView):
    model = ArtCollection
    context_object_name = 'collection'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        collection_to_show = get_object_or_404(ArtCollection, slug=self.kwargs['slug'])
        ap = []
        for item in collection_to_show.artpiece_set.all():
            ap += [item]
        context['artpieces'] = ap
        return context

class CodeProjectDetailView(DetailView):
    model = CodeProject
    context_object_name = 'project'

class ArtCollectionListView(ListView):
    model = ArtCollection
    template_name = 'portfolio/artcollection_list.html'
    context_object_name = 'collections'
    ordering = ['-date_created']
    paginate_by = 3

class ArtPieceListView(ListView):
    model = ArtPiece
    context_object_name = 'pieces'
    ordering = ['-date_created']
    paginate_by = 8

class CodeProjectListView(ListView):
    model = CodeProject
    context_object_name = 'projects'
    ordering = ['-date_created']
    paginate_by = 8
