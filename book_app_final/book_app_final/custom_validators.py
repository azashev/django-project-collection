from django.core.exceptions import ValidationError


def validate_username(username):
    if not username[0].isalpha():
        raise ValidationError("Username should start with a letter.")
    if username.isdigit():
        raise ValidationError("Username cannot be only numbers.")
    if not username.isalnum():
        raise ValidationError("Username should only contain letters and numbers.")
