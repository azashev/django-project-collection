from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from book_app_final.books_app.forms import BookForm
from book_app_final.books_app.models import Book
from book_app_final.reviews_app.forms import ReviewForm
from book_app_final.reviews_app.models import Review


@login_required
def book_catalogue(request):
    books = Book.objects.all()
    context = {
        'books': books,
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
        return redirect('book_catalogue')

    context = {
        'form': form,
    }

    return render(request, 'book_templates/add_book.html', context)


@login_required
def book_details(request, pk):
    book = Book.objects.get(pk=pk)
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
    pass


@login_required
def book_delete(request, pk):
    pass


@login_required
def book_shelf(request):
    pass
