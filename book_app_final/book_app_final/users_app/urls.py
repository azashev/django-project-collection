from django.urls import path

from book_app_final.users_app.views import ProfileView, ProfileUpdateView

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('update/', ProfileUpdateView.as_view(), name='update_profile')
]
