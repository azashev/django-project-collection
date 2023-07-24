from django.urls import path

from book_app_final.core_app.views import index
from book_app_final.users_app.views import UserRegisterView, UserLoginView

urlpatterns = [
    path('', index, name='homepage'),
    path('register/', UserRegisterView.as_view(), name='register_user'),
    path('login/', UserLoginView.as_view(), name='user_login'),
]
