from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def test_auth(request):
    username = "ade"
    password = "1234"

    user = User.objects.get(username=username)

    return JsonResponse({
        "exists": True,
        "is_active": user.is_active,
        "check_password": user.check_password(password),
        "authenticate": authenticate(username=username, password=password) is not None,
    })