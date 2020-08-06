from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
import stripe
from .models import ArtCollection, ArtPiece, Sizes, CodeProject
from .forms import ContactForm, AddToCartForm, RemoveFromCartForm
#from django.contrib.sessions import django-admin

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
                messages.error(request, "Bad header found, form not sent")
                return redirect("/")
            except Exception:
                messages.error(request,
                               "Error sending mail, please check your information and try again")
                return redirect("/")
            messages.success(request, "Your message has been sent!")
            return redirect("/")
    return render(request, "contactme.html", {'form': form})

def cartView(request):
    context = {}
    item_list = []
    order_total = 0
    if 'cart' in request.session and request.session['cart']:
        line_items = []
        for cart_item in request.session['cart']:
            piece_name = cart_item[0]
            size_pk = cart_item[1]
            try:
                piece = ArtPiece.objects.get(name=piece_name)
                size = Sizes.objects.get(pk=size_pk)
            except Exception:
                messages.error(request, "Cart error, your cart has been cleared")
                request.session.clear()
                return redirect("/")
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

        try:
            stripe.api_key = 'sk_test_51H2mBnGkKYIG13JoxGEM8rf5N1lF6tYST7h7DqrlwFrO64efz9EP4YhxqSsT6jQGHDhoXpIWkCGZtX06zdHjeozb00N5LC9UHu'
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='https://www.merriam-webster.com/dictionary/success',
                cancel_url='https://www.merriam-webster.com/dictionary/cancel',
            )
            context['session_id'] = session.id

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            #print(e)
            messages.warning(request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.warning(
                request, "A serious error occurred. We have been notifed.")
            return redirect("/")
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

def confirmationView(request, slug):
    item_list = []
    order_total = 0
    if 'cart' in request.session and request.session['cart']:
        line_items = []
        for cart_item in request.session['cart']:
            piece_name = cart_item[0]
            size_pk = cart_item[1]
            try:
                piece = ArtPiece.objects.get(name=piece_name)
                size = Sizes.objects.get(pk=size_pk)
            except Exception as e:
                messages.error(request, "Error getting items, your order has still been placed. ")
                request.session.clear()
                return redirect("/")
            price = piece.base_price + size.printing_price
            order_total += price
            item_list += [[piece, size, price]]
    context = {
        'order_number' : slug,
        'item_list' : item_list,
        'order_total' : order_total
    }
    request.session.clear()
    return render(request, 'portfolio/confirmation.html', context=context)

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
        art_piece_name = form.cleaned_data['piece']
        size_pk = form.cleaned_data['size']
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
