from django.urls import path

from book_app_final.users_app.views import ProfileView, ProfileUpdateView, ShelfView, ProfileDeleteView, \
    PasswordChangeView, ProfileBooksView, AddToShelfView, RemoveFromShelfView

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('delete/', ProfileDeleteView.as_view(), name='delete_user'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('my-books/', ProfileBooksView.as_view(), name='my_books'),
    path('shelf/', ShelfView.as_view(), name='shelf'),
    path('shelf/add-book/<int:pk>/', AddToShelfView.as_view(), name='add_to_shelf'),
    path('shelf/book-delete/<int:pk>/', RemoveFromShelfView.as_view(), name='remove_from_shelf'),
]
