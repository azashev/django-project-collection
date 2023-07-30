from django.urls import path

from book_app_final.books_app.views import book_add, book_catalogue, book_details, book_edit, book_delete

urlpatterns = [
    path('catalogue/', book_catalogue, name='book_catalogue'),
    path('add/', book_add, name='book_add'),
    path('details/<int:pk>/', book_details, name='book_details'),
    path('edit/<int:pk>/', book_edit, name='book_edit'),
    path('delete/<int:pk>/', book_delete, name='book_delete'),
]
