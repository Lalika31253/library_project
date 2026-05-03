from django import forms
from .models import Book, Visitor


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'author',
            'title',
            'category',
            'location',
            'visitor'
        ]


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = [
            'first_name',
            'last_name',
            'locations' 
        ]