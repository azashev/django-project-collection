from django.db import models

from book_app_final.books_app.models import Book
from book_app_final.users_app.models import CustomUser


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    review_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"
