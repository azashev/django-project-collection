from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth import models as auth_models
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
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    first_name = models.CharField(
        max_length=30,
        blank=True
    )

    last_name = models.CharField(
        max_length=30,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    is_superuser = models.BooleanField(
        default=False
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    bio = models.TextField(
        max_length=500,
        blank=True
    )

    location = models.CharField(
        max_length=30,
        blank=True
    )

    birth_date = models.DateField(
        null=True,
        blank=True
    )
