from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User
from django_ratelimit.exceptions import Ratelimited
from django.http import HttpResponseForbidden, HttpResponse


def validate_user_data(username, email, password, confirm_password):
    try:
        validate_email(email)
    except ValidationError:
        return "Invalid email format."

    if password != confirm_password:
        return "Passwords do not match."

    if len(password) < 8:
        return "Password must be at least 8 characters long."

    if not re.search(r'[A-Za-z]', password):
        return "Password must contain at least one letter."

    if not re.search(r'[0-9]', password):
        return "Password must contain at least one number."

    if User.objects.filter(username=username).exists():
        return "Username already exists."

    if User.objects.filter(email=email).exists():
        return "Email already exists."

    return None

def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return HttpResponse('Sorry you are blocked', status=429)
    return HttpResponseForbidden('Forbidden')