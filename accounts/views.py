from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User

def test_auth(request):
    return JsonResponse({
        "db_name": settings.DATABASES["default"]["NAME"],
        "db_host": settings.DATABASES["default"]["HOST"],
        "users": list(User.objects.values("id", "username", "email")),
    })