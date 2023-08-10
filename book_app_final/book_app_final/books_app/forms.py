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

    # Validation
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title.strip():
            raise forms.ValidationError("Title cannot be only whitespace.")
        return title


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

    search = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for a book...'
            })
    )
