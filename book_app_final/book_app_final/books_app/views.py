from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from book_app_final.books_app.forms import BookForm, CatalogueFilterForm
from book_app_final.books_app.models import Book
from book_app_final.reviews_app.forms import ReviewForm
from book_app_final.reviews_app.models import Review


@login_required
def book_catalogue(request):
    books = Book.objects.all()
    form = CatalogueFilterForm(request.GET)

    author_query = request.GET.get('author')
    genre_query = request.GET.get('genre')
    sort_by = request.GET.get('sort_by')

    if author_query:
        books = books.filter(author__id=author_query)

    if genre_query:
        books = books.filter(genres__id=genre_query)

    if sort_by:
        books = books.order_by(sort_by)

    books_with_genres = []

    for book in books:
        book_genres = ", ".join([genre.genre_name for genre in book.genres.all()])
        books_with_genres.append({
            'title': book.title,
            'image': book.book_image,
            'description': book.description,
            'genres': book_genres,
            'author': book.author,
            'pk': book.pk,
            'added_by': book.created_by.username,
        })

    context = {
        'form': form,
        'books': books_with_genres,
    }

    return render(request, 'book_templates/catalogue.html', context)


@login_required
def book_add(request):
    form = BookForm(request.POST or None)

    if form.is_valid():
        book = form.save(commit=False)
        user = request.user
        book.created_by = user
        book.save()
        form.save_m2m()
        return redirect('book_catalogue')

    context = {
        'form': form,
    }

    return render(request, 'book_templates/add_book.html', context)


@login_required
def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    review_form = ReviewForm(request.POST or None)

    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.user = request.user
        review.book = book
        review.save()
        return redirect('book_details', pk=pk)

    reviews = Review.objects.filter(book=book)
    context = {
        'book': book,
        'reviews': reviews,
        'review_form': review_form,
    }

    return render(request, 'book_templates/book_details.html', context)


@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if not book.created_by == request.user:
        return redirect('my_books')

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.save()
            form.save_m2m()
            return redirect('my_books')
    else:
        form = BookForm(instance=book)

    context = {
        'book': book,
        'form': form,
    }

    return render(request, 'book_templates/book_edit.html', context)


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if not book.created_by == request.user:
        return redirect('my_books')

    if request.method == 'POST':
        book.delete()
        return redirect('my_books')

    else:
        context = {
            'book': book,
        }
        return render(request, 'book_templates/book_delete.html', context)
