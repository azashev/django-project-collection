from django.urls import path

from book_app_final.reviews_app.views import delete_review

urlpatterns = [
    path('<int:pk>/delete/', delete_review, name='review_delete'),
]
