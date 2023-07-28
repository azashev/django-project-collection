from django import forms

from book_app_final.books_app.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genres', 'description', 'author', 'book_image']
        labels = {
            'author': 'Author',
            'book_image': 'Image',
            '': '',
        }

        widgets = {
            'book_image': forms.URLInput(attrs={'placeholder': 'Enter URL'}),
        }
