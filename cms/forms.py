from django import forms
from .models import Product, Category , Order, OrderItem


class SearchForm(forms.Form):
    q = forms.CharField()
