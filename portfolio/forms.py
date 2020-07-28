from django import forms
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from .models import ArtPiece, Sizes

def piece_validator(piece):
    try:
        ArtPiece.objects.get(name=piece)
    except ObjectDoesNotExist:
        raise ValidationError(_('No such art piece!'))

def size_validator(size):
    try:
        Sizes.objects.get(size=size)
    except ObjectDoesNotExist:
        raise ValidationError(_('No such size!'))

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea, required=True)

class AddToCartForm(forms.Form):
    piece = forms.CharField(widget=forms.HiddenInput, max_length=100, validators=[piece_validator])
    size = forms.CharField(max_length=10, validators=[size_validator])
    def clean(self):
        cleaned_data = super().clean()
        piece = cleaned_data.get("piece")
        size = cleaned_data.get("size")
        piece_object = ArtPiece.objects.get(name=piece)
        if piece and size:
            # Only do something if both fields are valid so far.
            size_flag = False
            for piece_size in piece_object.size_options.all():
                if size == piece_size.size:
                    size_flag = True
            if not size_flag:
                raise forms.ValidationError(_("That piece isn't available in that size!"))

class RemoveFromCartForm(forms.Form):
    piece = forms.CharField(max_length=100, validators=[piece_validator])
    size = forms.CharField(max_length=10, validators=[size_validator])
