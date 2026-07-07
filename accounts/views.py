from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def test_auth(request):
    try:
        username = "ade"
        password = "1234"  # Replace with the actual password

        user = User.objects.get(username=username)

        return JsonResponse({
            "exists": True,
            "username": user.username,
            "is_active": user.is_active,
            "check_password": user.check_password(password),
            "authenticate": authenticate(
                username=username,
                password=password
            ) is not None,
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "type": type(e).__name__,
        }, status=500)