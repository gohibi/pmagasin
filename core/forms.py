from django import forms
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Laissez un commentaire','id':'text-review'}))

    class Meta:
        model = ProductReview
        fields = ['review','rating']