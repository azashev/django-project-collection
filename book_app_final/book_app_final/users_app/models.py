from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth import models as auth_models
from django.core.validators import FileExtensionValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    username = models.CharField(
        max_length=30,
        unique=True,
        help_text='Required. Please make sure to enter a valid username',
    )

    email = models.EmailField(
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_superuser = models.BooleanField(
        default=False,
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        'CustomUser',
        on_delete=models.CASCADE,
    )

    first_name = models.CharField(
        max_length=30,
        blank=True,
        default="",
    )

    last_name = models.CharField(
        max_length=30,
        blank=True,
        default="",
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
    )

    location = models.CharField(
        max_length=30,
        blank=True,
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        validators=[FileExtensionValidator(
            allowed_extensions=[
                'jpg', 'jpeg', 'png'
            ]
        )],
        default='profile_pics/default.jpg'
    )

    is_default_image = models.BooleanField(
        default=True,
    )

    def get_first_name(self):
        return self.first_name if self.first_name is not None else ""

    def get_last_name(self):
        return self.last_name if self.last_name is not None else ""


class Shelf(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shelf',
    )

    books = models.ManyToManyField(
        'books_app.Book',
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}'s Shelf"
