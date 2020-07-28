from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.core.mail import send_mail, BadHeaderError
from .models import ArtCollection, ArtPiece, Sizes, CodeProject
from .forms import ContactForm, AddToCartForm, RemoveFromCartForm
import stripe
#from django.contrib.sessions import django-addmin

def clearCartView(request):
    request.session.clear()
    return redirect('cart_list')

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
    return HttpResponse('Success!')

def failure(request):
    return HttpResponse('Failure! Something went wrong.')

def cartView(request):
    context = {}
    item_list = []
    order_total = 0
    if 'cart' in request.session and request.session['cart']:
        line_items = []
        for cart_item in request.session['cart']:
            piece_name = cart_item[0]
            size_pk = cart_item[1]
            piece = get_object_or_404(ArtPiece, name=piece_name)
            size = get_object_or_404(Sizes, pk=size_pk)
            price = piece.base_price + size.printing_price
            order_total += price
            item_list += [[piece, size, price]]
            product_data = {
                'name' : piece.name,
                'description' : piece.description,
                'images' : ['https://www.desicomments.com/wp-content/uploads/2017/02/Bart-simpson-Driving.jpg'] #[piece.image.url]
            }
            price_data = {
                'currency' : 'usd',
                'product_data' : product_data,
                'unit_amount' : int(price * 100)
            }
            line_items += [{
                'price_data' : price_data,
                'quantity' : 1
            }]
        stripe.api_key = 'sk_test_51H2mBnGkKYIG13JoxGEM8rf5N1lF6tYST7h7DqrlwFrO64efz9EP4YhxqSsT6jQGHDhoXpIWkCGZtX06zdHjeozb00N5LC9UHu'
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://www.merriam-webster.com/dictionary/success',
            cancel_url='https://www.merriam-webster.com/dictionary/cancel',
        )
        context['session_id'] = session.id
    else:
        item_list = []
        order_total = 0
        request.session['cartCount'] = 0
        request.session['cart'] = []

    if request.method == 'GET':
        form = RemoveFromCartForm()
    else:
        form = RemoveFromCartForm(request.POST)
        if form.is_valid():
            art_piece_name = form.cleaned_data['piece']
            size_pk = form.cleaned_data['size']
            if 'cart' in request.session and request.session['cart']:
                index = 0
                for item in request.session['cart']:
                    if item[0] == art_piece_name and item[1] == size_pk:
                        cart = request.session['cart']
                        cart.pop(index)
                        request.session['cart'] = cart
                        request.session['cartCount'] = request.session['cartCount'] - 1
                        return redirect(request.path_info)
                    index += 1

    context.update({
        'form' : form,
        'item_list' : item_list,
        'order_total' : order_total,
    })

    return render(request, 'portfolio/cart.html', context=context)

class ArtPieceDetailControllView(View):
    def get(self, request, *args, **kwargs):
        view = ArtPieceDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ArtPieceFormView.as_view()
        return view(request, *args, **kwargs)

class ArtPieceDetailView(DetailView):
    model = ArtPiece
    context_object_name = 'object'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddToCartForm()
        return context

class ArtPieceFormView(SingleObjectMixin, FormView):
    template_name = 'portfolio/artpiece_detail.html'
    form_class = AddToCartForm
    model = ArtPiece
    def form_valid(self, form):
        #if self.object.name != form.cleaned_data['piece']:
        #    return HttpResponse(self.object.name)
        art_piece_name = form.cleaned_data['piece']
        size_pk = form.cleaned_data['size']
        #if size_to_add not in art_piece_to_add.size_options_set.all():
        #    return super().form_valid(form)
        if 'cart' in self.request.session and self.request.session['cart']:
            self.request.session['cart'] += [[art_piece_name, size_pk]]
        else:
            self.request.session['cart'] = []
            self.request.session['cart'] += [[art_piece_name, size_pk]]
        if 'cartCount' in self.request.session and self.request.session['cartCount']:
            self.request.session['cartCount'] += 1
        else:
            self.request.session['cartCount'] = 1
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('art_piece_detail', kwargs={'slug': self.object.slug})

class ArtCollectionDetailView(DetailView):
    model = ArtCollection
    context_object_name = 'collection'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the art collection
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
