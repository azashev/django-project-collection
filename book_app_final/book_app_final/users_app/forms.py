from django import forms
from django.contrib.auth import forms as auth_forms

from book_app_final.custom_validators import validate_username
from book_app_final.users_app.models import CustomUser, Profile


class SignUpForm(auth_forms.UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Required. Please make sure to enter a valid username',
        validators=[validate_username],
    )

    email = forms.EmailField(
        max_length=255,
        help_text='Required. Please make sure to enter a valid email address',
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Required. Please make sure to enter a valid username',
        validators=[validate_username],
    )

    email = forms.EmailField(
        max_length=255,
        required=True,
        help_text='Please make sure to enter a valid email address',
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        ),
    )

    profile_picture = forms.ImageField(
        required=False,
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'location', 'birth_date', 'profile_picture']
