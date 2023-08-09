from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from book_app_final.books_app.models import Author, Book, Genre


def index(request):
    return render(request, 'core_templates/index.html')


class AuthorsView(auth_mixins.LoginRequiredMixin, ListView):
    model = Author
    template_name = 'core_templates/authors.html'


class AuthorBooksView(auth_mixins.LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'core_templates/author_books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.object
        genre_query = self.request.GET.get('genre')
        books = Book.objects.filter(author=author)

        if genre_query:
            genre = get_object_or_404(Genre, id=genre_query)
            books = books.filter(genres__in=[genre])

        context['books'] = books
        context['genres'] = Genre.objects.all()

        return context


def custom_404_view(request, exception):
    messages.warning(request, "The item you're looking for doesn't exist or has been removed.")
    return redirect('homepage')
