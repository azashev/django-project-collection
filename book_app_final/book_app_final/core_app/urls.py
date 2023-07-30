from django.urls import path

from book_app_final.core_app.views import index, AuthorsView, AuthorBooksView
from book_app_final.users_app.views import UserRegisterView, UserLoginView, UserLogoutView

urlpatterns = [
    path('', index, name='homepage'),
    path('register/', UserRegisterView.as_view(), name='register_user'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('authors/', AuthorsView.as_view(), name='authors'),
    path('author-books/<slug:slug>', AuthorBooksView.as_view(), name='author_books'),
]
