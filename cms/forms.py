from django import forms
from .models import Product, Category , Order, OrderItem


class SearchForm(forms.Form):
    q = forms.CharField()
    #c = forms.ModelChoiceField(queryset=Category.objects.all().order_by('category'))

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['c'].label = ''
    #     self.fields['c'].required = False
    #     self.fields['c'].label = 'Category'
    #     self.fields['q'].label = 'Search For'
    #     self.fields['q'].widget.attrs.update(
    #         {'class': 'form-control'})