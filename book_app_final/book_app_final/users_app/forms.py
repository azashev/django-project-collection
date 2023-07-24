from django import forms
from django.contrib.auth import forms as auth_forms

from book_app_final.users_app.models import CustomUser


class SignUpForm(auth_forms.UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        help_text='Required. Please enter a valid email address.'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',)
