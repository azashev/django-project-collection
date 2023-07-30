from django import forms

from book_app_final.books_app.models import Book, Author, Genre


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genres', 'description', 'author', 'book_image']
        labels = {
            'author': 'Author',
            'book_image': 'Image',
        }

        widgets = {
            'book_image': forms.URLInput(attrs={'placeholder': 'Enter URL'}),
        }


class CatalogueFilterForm(forms.Form):
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
    )

    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
    )

    sort_by = forms.ChoiceField(
        choices=[
            ('', '---------'),
            ('title', 'Title'),
            ('author', 'Author')
        ],
        required=False
    )
