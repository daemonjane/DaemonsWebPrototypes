import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.cache import cache
from django.db import models as db_models
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem, Order, OrderItem, OrderTracking, ProductAddon, TrackingHistory, Wishlist
from .serializers import CartSerializer, OrderSerializer
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


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def auth_password_reset_request(request):
    """Send a password reset email with a token + uidb64 link."""
    email = request.data.get("email", "").strip()
    if not email:
        return Response({"error": "Email is required."}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "If that email is registered, a reset link has been sent."})

    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    protocol = "https" if request.is_secure() else "http"
    reset_url = f"{protocol}://{current_site.domain}/reset-password/{uidb64}/{token}/"

    subject = "Password Reset — TechStore"
    message = render_to_string("registration/password_reset_email.html", {
        "user": user,
        "protocol": protocol,
        "domain": current_site.domain,
        "uid": uidb64,
        "token": token,
    })
    html_message = f"""
    <p>Hi {user.username},</p>
    <p>Click the link below to reset your password:</p>
    <p><a href="{reset_url}">{reset_url}</a></p>
    <p>If you didn't request this, you can ignore this email.</p>
    """
    send_mail(subject, message, None, [email], html_message=html_message)

    return Response({"message": "If that email is registered, a reset link has been sent."})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def auth_password_reset_confirm(request, uidb64, token):
    """Confirm a password reset using uidb64 + token from the email link."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({"error": "Invalid reset link."}, status=400)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired reset link."}, status=400)

    password = request.data.get("password", "")
    if len(password) < 8:
        return Response({"error": "Password must be at least 8 characters."}, status=400)

    user.set_password(password)
    user.save()
    return Response({"message": "Password has been reset successfully."})

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def auth_register(request):
    """Register a new user account."""
    data = request.data
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
    ip = request.META.get("REMOTE_ADDR", "unknown")
    cache_key = f"login_rate:{ip}"
    attempts = cache.get(cache_key, 0)
    if attempts >= 5:
        return Response({"error": "Too many login attempts. Try again later."}, status=429, headers={"Retry-After": "300", "X-RateLimit-Reset": "300"})

    data = request.data

    username = data.get("username", "")
    password = data.get("password", "")
    user = authenticate(request, username=username, password=password)

    if user is None:
        cache.set(cache_key, attempts + 1, 300)
        remaining = 4 - attempts
        return Response({"error": "Invalid username or password."}, status=401, headers={"X-RateLimit-Remaining": str(remaining)})

    cache.delete(cache_key)
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

    data = request.data
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


# ---------------------------------------------------------------------------
# Cart
# ---------------------------------------------------------------------------

def _get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def _cart_json(cart):
    """Serialize cart with a fresh DB hit to avoid stale prefetch caches."""
    fresh = Cart.objects.get(pk=cart.pk)
    return CartSerializer(fresh).data


@api_view(['GET'])
def cart_get(request):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)
    return Response(_cart_json(_get_cart(request.user)))


@api_view(['POST'])
def cart_add(request):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)

    data = request.data
    cart = _get_cart(request.user)
    item_type = data.get("item_type", "product")
    name = data.get("name", "")
    price = data.get("price", 0)
    quantity = int(data.get("quantity", 1))
    image = data.get("image", "")

    existing = cart.items.filter(
        item_type=item_type,
        name=name,
    ).first()

    if existing and item_type == "addon":
        return Response({"error": "Add-on already in cart."}, status=409)

    if existing:
        existing.quantity += quantity
        existing.save()
    else:
        CartItem.objects.create(
            cart=cart,
            name=name,
            price=price,
            quantity=quantity,
            image=image,
            item_type=item_type,
        )

    return Response(_cart_json(cart))


@api_view(['PATCH', 'DELETE'])
def cart_item_detail(request, item_id):
    """Update or remove a specific cart item."""
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)

    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found."}, status=404)

    if request.method == 'DELETE':
        item.delete()
        return Response(_cart_json(_get_cart(request.user)))

    data = request.data
    if "quantity" in data:
        item.quantity = max(0, int(data["quantity"]))
    if "price" in data:
        item.price = data["price"]
    if "name" in data:
        item.name = data["name"]
    item.save()

    if item.quantity <= 0:
        item.delete()

    return Response(_cart_json(_get_cart(request.user)))


@api_view(['POST'])
def cart_clear(request):
    """Remove all items from the cart."""
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)
    cart = _get_cart(request.user)
    cart.items.all().delete()
    return Response(_cart_json(_get_cart(request.user)))


@api_view(['POST'])
def cart_merge(request):
    """Merge localStorage cart items into server cart after login."""
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)

    data = request.data
    cart = _get_cart(request.user)
    local_items = data.get("items", [])

    for local in local_items:
        item_type = local.get("item_type") or local.get("type", "product")
        name = local.get("name", "")
        price = local.get("price", 0)
        quantity = int(local.get("quantity", 1))
        image = local.get("image", "")

        existing = cart.items.filter(item_type=item_type, name=name).first()
        if existing:
            existing.quantity += quantity
            existing.save()
        else:
            CartItem.objects.create(
                cart=cart, name=name, price=price,
                quantity=quantity, image=image, item_type=item_type,
            )

    return Response(_cart_json(cart))


# ---------------------------------------------------------------------------
# Wishlist
# ---------------------------------------------------------------------------

def _get_wishlist(user):
    """Get or create wishlist for the current user."""
    wishlist, _ = Wishlist.objects.get_or_create(user=user)
    return wishlist


@api_view(['GET'])
def wishlist_get(request):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)
    wishlist = _get_wishlist(request.user)
    return Response({"product_slugs": wishlist.product_slugs})


@api_view(['POST'])
def wishlist_toggle(request):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)

    data = request.data
    slug = data.get("slug")
    if not slug:
        return Response({"error": "slug is required."}, status=400)

    wishlist = _get_wishlist(request.user)
    slugs = list(wishlist.product_slugs)
    if slug in slugs:
        slugs.remove(slug)
        added = False
    else:
        slugs.append(slug)
        added = True

    wishlist.product_slugs = slugs
    wishlist.save(update_fields=["product_slugs"])
    return Response({"added": added, "product_slugs": slugs})


@api_view(['GET'])
def wishlist_check(request, slug):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)
    wishlist = _get_wishlist(request.user)
    return Response({"is_favorite": slug in wishlist.product_slugs})


# ---------------------------------------------------------------------------
# Orders
# ---------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def order_detail(request, pk):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=404)
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(['POST'])
def order_checkout(request):
    data = request.data
    name = data.get("name", "")
    email = data.get("email", "")
    address = data.get("address", "")

    if not name or not email:
        return Response({"error": "Name and email are required."}, status=400)
    if not address:
        return Response({"error": "Shipping address is required."}, status=400)

    items_data = data.get("items")
    if not items_data:
        return Response({"error": "Cart is empty."}, status=400)

    gift_card_code = data.get("gift_card_code", "")
    gift_card_discount = data.get("gift_card_discount")

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        email=email,
        name=name,
        address=address,
        gift_card_code=gift_card_code,
        gift_card_discount=gift_card_discount,
    )

    for item_data in items_data:
        OrderItem.objects.create(
            order=order,
            name=item_data.get("name", ""),
            price=item_data.get("price", 0),
            quantity=item_data.get("quantity", 1),
            item_type=item_data.get("item_type", "product"),
        )

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=201)


# ---------------------------------------------------------------------------
# Tracking
# ---------------------------------------------------------------------------

@api_view(['GET'])
def order_tracking(request, pk):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=404)

    try:
        tracking = order.tracking
        history = tracking.history.all()
        return Response({
            "order_id": order.pk,
            "tracking_number": tracking.tracking_number,
            "carrier": tracking.carrier,
            "tracking_url": tracking.tracking_url,
            "estimated_delivery": tracking.estimated_delivery.isoformat() if tracking.estimated_delivery else None,
            "delivered_at": tracking.delivered_at.isoformat() if tracking.delivered_at else None,
            "current_status": order.get_status_display(),
            "history": [
                {
                    "status": h.status,
                    "location": h.location,
                    "note": h.note,
                    "timestamp": h.timestamp.isoformat(),
                }
                for h in history
            ],
        })
    except OrderTracking.DoesNotExist:
        return Response({"tracking_number": None, "carrier": None, "tracking_url": None, "history": []})


# ---------------------------------------------------------------------------
# Product Add-ons
# ---------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def product_addons(request, slug):
    addons = ProductAddon.objects.filter(product_slug=slug, is_available=True)
    data = [
        {
            "id": a.pk,
            "name": a.name,
            "description": a.description,
            "price": float(a.price),
            "image": a.image,
        }
        for a in addons
    ]
    return Response({"addons": data})

@api_view(['GET'])
@permission_classes([AllowAny])
def api_version(request):
    return Response({"version": "1.0.0", "api": "techstore"})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def newsletter_subscribe(request):
    import re
    from website.models import NewsletterSubscription
    email = request.data.get("email", "").strip()
    if not email:
        return Response({"error": "Email is required."}, status=400)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return Response({"error": "Invalid email format."}, status=400)
    subscription, created = NewsletterSubscription.objects.get_or_create(
        email=email, defaults={"active": True},
    )
    if created:
        return Response({"message": "Subscribed successfully."}, status=201)
    if not subscription.active:
        subscription.active = True
        subscription.save()
        return Response({"message": "Subscription reactivated."})
    return Response({"message": "Already subscribed."})
