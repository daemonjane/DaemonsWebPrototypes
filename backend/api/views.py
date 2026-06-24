import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from website.models import UserProfile


def _user_data(user):
    """Build a user data dict safe for API responses."""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "profile": {
            "bio": user.profile.bio if hasattr(user, "profile") else "",
            "location": user.profile.location if hasattr(user, "profile") else "",
            "phone": user.profile.phone if hasattr(user, "profile") else "",
            "avatar_url": user.profile.avatar_url if hasattr(user, "profile") else "",
        } if hasattr(user, "profile") else {},
    }


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok'})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def auth_register(request):
    """Register a new user account."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return Response({"error": "Invalid JSON body."}, status=400)

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not username or not email or not password:
        return Response({"error": "Username, email, and password are required."}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken."}, status=409)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered."}, status=409)

    user = User.objects.create_user(username=username, email=email, password=password)
    UserProfile.objects.create(user=user)

    login(request, user)
    return Response(_user_data(user), status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def auth_login(request):
    """Authenticate and log in a user."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return Response({"error": "Invalid JSON body."}, status=400)

    username = data.get("username", "")
    password = data.get("password", "")
    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response({"error": "Invalid username or password."}, status=401)

    login(request, user)
    return Response(_user_data(user))


@api_view(['POST'])
def auth_logout(request):
    """Log out the current user."""
    logout(request)
    return Response({"status": "logged out"})


@api_view(['GET', 'PATCH'])
def auth_profile(request):
    """Get or update the current user's profile."""
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)

    if request.method == 'GET':
        return Response(_user_data(request.user))

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return Response({"error": "Invalid JSON body."}, status=400)

    user = request.user
    if "email" in data:
        new_email = data["email"].strip()
        if new_email and new_email != user.email:
            if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                return Response({"error": "Email already in use."}, status=409)
            user.email = new_email

    if "username" in data:
        new_username = data["username"].strip()
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                return Response({"error": "Username already taken."}, status=409)
            user.username = new_username

    user.save()

    profile, _ = UserProfile.objects.get_or_create(user=user)
    for field in ("bio", "location", "phone", "avatar_url"):
        if field in data:
            setattr(profile, field, data[field])
    profile.save()

    return Response(_user_data(user))


@api_view(['GET'])
@ensure_csrf_cookie
def csrf_token(request):
    """Return a CSRF token for the client."""
    return Response({"csrfToken": get_token(request)})
