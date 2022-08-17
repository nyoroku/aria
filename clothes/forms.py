from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import Product, Image, Feature, Size
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField
from dal import autocomplete


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name',
                  'price', 'stock', 'available', 'type', 'edit', 'brand', 'shop', 'category', 'subcategory',
                  'description', 'picture',
                  )

ImageFormSet = inlineformset_factory(Product, Image, fields=['color', 'image'], extra=3, can_delete=True)

FeatureFormSet = inlineformset_factory(Product, Feature, fields=['name', ], extra=3, can_delete=True)

SizeFormSet = inlineformset_factory(Product, Size, fields=['name', ], extra=3, can_delete=True)