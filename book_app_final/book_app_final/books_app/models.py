from django.contrib.auth import models as auth_models
from django.db import models

from book_app_final.users_app.models import CustomUser


class Author(models.Model):
    author_name = models.CharField(
        max_length=200
    )

    def __str__(self):
        return self.author_name


class Book(models.Model):
    title = models.CharField(
        max_length=200
    )

    authors = models.ManyToManyField(
        Author
    )

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title
