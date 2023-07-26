from django.urls import path

from book_app_final.users_app.views import ProfileView, ProfileUpdateView, ShelfView, ProfileDeleteView, \
    PasswordChangeView, PasswordChangedView

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('delete/', ProfileDeleteView.as_view(), name='delete_user'),
    path('shelf/', ShelfView.as_view(), name='shelf'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-changed/', PasswordChangedView.as_view(), name='password_changed'),
]
