from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.cache import cache
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response

from services.osimart import OsimartClient, OsimartError
from website.models import NewsletterSubscription
import logging
import re
import stripe

logger = logging.getLogger(__name__)


class IsStaffOrAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

from .models import Order, OrderItem, OrderTracking, ProductAddon, TrackingHistory, Wishlist
from .serializers import OrderSerializer
from website.models import UserProfile


def _user_data(user):
    """Build a user data dict safe for API responses."""
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "profile": {
            "bio": profile.bio,
            "location": profile.location,
            "phone": profile.phone,
            "avatar_url": profile.avatar_url,
            "osimart_customer_id": profile.osimart_customer_id or "",
        },
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request):
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "Not authenticated."}, status=401)
    old = request.data.get("old_password", "")
    new = request.data.get("new_password", "")
    if not old or not new:
        return Response({"error": "old_password and new_password are required."}, status=400)
    if not user.check_password(old):
        return Response({"error": "Old password is incorrect."}, status=403)
    user.set_password(new)
    user.save()
    return Response({"detail": "Password changed successfully."})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    email = (request.data.get("email") or "").strip()
    code = (request.data.get("code") or "").strip()
    new_password = request.data.get("new_password", "")
    if not email or not code or not new_password:
        return Response({"error": "email, code, and new_password are required."}, status=400)
    cache_key = f"password_reset_code:{email}"
    stored = cache.get(cache_key)
    if not stored or str(stored) != str(code):
        return Response({"error": "Invalid or expired code."}, status=400)
    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"error": "No user with that email."}, status=404)
    user.set_password(new_password)
    user.save()
    cache.delete(cache_key)
    return Response({"detail": "Password reset successfully."})


@api_view(['POST'])
@permission_classes([AllowAny])
def osimart_sync(request):
    """Create/find local Django user after successful Osimart authentication."""
    data = request.data
    email = (data.get("email") or "").strip()
    osimart_customer_id = (data.get("osimart_customer_id") or "").strip()
    name = (data.get("name") or "").strip()
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    if not first_name and name:
        parts = name.split()
        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

    if not email:
        return Response({"error": "Email is required."}, status=400)

    user = User.objects.filter(email=email).first()
    if not user:
        username = email.split("@")[0]
        base = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base}_{counter}"
            counter += 1
        user = User.objects.create_user(
            username=username, email=email,
            first_name=first_name, last_name=last_name,
        )

    profile, _ = UserProfile.objects.get_or_create(user=user)
    if osimart_customer_id:
        profile.osimart_customer_id = osimart_customer_id
        profile.save(update_fields=["osimart_customer_id"])

    login(request, user)

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "profile": {
            "bio": profile.bio,
            "location": profile.location,
            "phone": profile.phone,
            "avatar_url": profile.avatar_url,
            "osimart_customer_id": profile.osimart_customer_id,
        },
    })


@api_view(['GET'])
def auth_csrf(request):
    return Response({'csrfToken': get_token(request)})

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok'})


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


@api_view(['POST'])
@permission_classes([AllowAny])
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

def _rate_limit_check(request, cache_key_prefix, max_attempts=3, cooldown=300):
    ip = request.META.get("REMOTE_ADDR", "unknown")
    cache_key = f"{cache_key_prefix}:{ip}"
    attempts = cache.get(cache_key, 0)
    if attempts >= max_attempts:
        return Response({"error": "Too many attempts. Try again later."}, status=429, headers={"Retry-After": str(cooldown)})
    cache.set(cache_key, attempts + 1, cooldown)
    return None


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_register(request):
    """Register a new user — sends OTP via Osimart, does NOT create local user yet."""
    rate = _rate_limit_check(request, "register_rate")
    if rate:
        return rate
    data = request.data
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    first_name = data.get("first_name", "").strip() or username
    last_name = data.get("last_name", "").strip() or first_name.split()[-1] if first_name.split() else "_"

    if not username or not email or not password:
        return Response({"error": "Username, email, and password are required."}, status=400)

    if len(password) < 8:
        return Response({"error": "Password must be at least 8 characters."}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken."}, status=409)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered."}, status=409)

    try:
        client = OsimartClient()
        logger.info("Registering customer on Osimart for %s", email)
        osimart_resp = client.register_customer(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        logger.info("Osimart registration pending: %s", osimart_resp)
    except OsimartError as e:
        logger.error("Osimart registration failed: %s", e)
        detail = e.response_body or str(e)
        return Response({"error": f"Registration failed — {detail}"}, status=e.status_code if isinstance(e.status_code, int) else 502)
    except Exception as e:
        logger.exception("Unexpected error during Osimart registration")
        return Response({"error": f"Registration failed: {e}"}, status=502)

    request.session['pending_registration'] = {
        'username': username,
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
    }
    request.session.modified = True

    return Response({"status": "pending", "email": email, "message": "OTP sent to email."}, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_verify(request):
    """Verify OTP and complete registration — creates local user + Osimart customer."""
    rate = _rate_limit_check(request, "verify_rate", max_attempts=5)
    if rate:
        return rate
    email = request.data.get("email", "").strip()
    code = request.data.get("code", "").strip()

    if not email or not code:
        return Response({"error": "Email and code are required."}, status=400)

    pending = request.session.get('pending_registration')
    if not pending or pending.get('email') != email:
        return Response({"error": "No pending registration found for this email. Please register again."}, status=400)

    try:
        client = OsimartClient()
        verify_resp = client.verify_otp(email=email, code=code)
    except OsimartError as e:
        logger.error("OTP verify failed: %s", e)
        detail = e.response_body or str(e)
        return Response({"error": f"Verification failed — {detail}"}, status=e.status_code if isinstance(e.status_code, int) else 400)
    except Exception as e:
        logger.exception("Unexpected error during OTP verification")
        return Response({"error": f"Verification failed: {e}"}, status=502)

    username = pending['username']
    password = pending['password']
    first_name = pending.get('first_name', username)
    last_name = pending.get('last_name', '')

    try:
        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name,
        )
        profile = UserProfile.objects.create(user=user)
        osimart_customer_id = verify_resp.get("customer", {}).get("id") if isinstance(verify_resp, dict) else None
        if osimart_customer_id:
            profile.osimart_customer_id = str(osimart_customer_id)
            profile.save(update_fields=["osimart_customer_id"])
        else:
            customer_id = verify_resp.get("id") if isinstance(verify_resp, dict) else None
            if customer_id:
                profile.osimart_customer_id = str(customer_id)
                profile.save(update_fields=["osimart_customer_id"])
    except Exception as e:
        logger.exception("Local user creation failed after OTP verify")
        return Response({"error": "Verification succeeded but account creation failed. Please contact support."}, status=502)

    login(request, user)

    access_token = None
    refresh_token = None
    try:
        client = OsimartClient()
        osimart_data = client.customer_login(email=email, password=password, device_name="web")
        access_token = osimart_data.get("access_token")
        refresh_token = osimart_data.get("refresh_token")
    except Exception:
        pass

    del request.session['pending_registration']
    request.session.modified = True

    resp_data = _user_data(user)
    if access_token:
        resp_data["osimart_token"] = access_token
        resp_data["osimart_refresh_token"] = refresh_token

    return Response(resp_data, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_resend_otp(request):
    """Resend OTP for a pending registration."""
    rate = _rate_limit_check(request, "resend_rate", max_attempts=3, cooldown=120)
    if rate:
        return rate
    email = request.data.get("email", "").strip()
    if not email:
        return Response({"error": "Email is required."}, status=400)

    pending = request.session.get('pending_registration')
    if not pending or pending.get('email') != email:
        return Response({"error": "No pending registration found for this email."}, status=400)

    try:
        client = OsimartClient()
        client.resend_otp(email=email)
        return Response({"message": "OTP resent to email."})
    except OsimartError as e:
        logger.error("OTP resend failed: %s", e)
        detail = e.response_body or str(e)
        return Response({"error": f"Failed to resend OTP — {detail}"}, status=e.status_code if isinstance(e.status_code, int) else 502)
    except Exception as e:
        logger.exception("Unexpected error resending OTP")
        return Response({"error": f"Failed to resend OTP: {e}"}, status=502)


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_guest_login(request):
    """Create a guest session (no password, no local User)."""
    first_name = request.data.get("first_name", "").strip()
    last_name = request.data.get("last_name", "").strip()
    email = request.data.get("email", "").strip()

    if not first_name:
        return Response({"error": "First name is required for guest login."}, status=400)

    try:
        client = OsimartClient()
        logger.info("Creating guest Osimart customer for %s", email)
        client.create_customer({
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "is_guest": True,
            "mobile_number": "0000000000",
        })
    except OsimartError as e:
        logger.error("Guest customer creation failed: %s", e)
        detail = e.response_body or str(e)
        return Response({"error": f"Guest login failed — Osimart error: {detail}"}, status=502)
    except Exception as e:
        logger.exception("Unexpected error creating guest customer")
        return Response({"error": f"Guest login failed: {e}"}, status=502)

    request.session["guest_email"] = email
    request.session["guest_first_name"] = first_name
    request.session["guest_last_name"] = last_name
    return Response({"email": email, "first_name": first_name, "last_name": last_name})


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_staff_login(request):
    """Authenticate and log in a staff user (Django session-based)."""
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    user = authenticate(request, username=username, password=password)
    if user is None or not user.is_staff:
        return Response({"error": "Invalid credentials or not a staff user."}, status=401)
    login(request, user)
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def osimart_login(request):
    """Authenticate via Osimart API, create/find local user, and log in."""
    data = request.data
    login_field = data.get("login_field") or data.get("email") or data.get("username", "")
    password = data.get("password", "")
    if not login_field or not password:
        return Response({"error": "Email or username and password are required."}, status=400)

    osimart_data = None
    try:
        client = OsimartClient()
        osimart_data = client.customer_login(
            email=login_field,
            password=password,
            device_name=data.get("device_name", "web"),
            device_id=data.get("device_id", ""),
        )
    except OsimartError:
        pass

    if osimart_data and osimart_data.get("access_token"):
        access_token = osimart_data["access_token"]
        email = login_field if "@" in login_field else ""
        user = User.objects.filter(email=email).first() if email else None
        if not user:
            user, _ = User.objects.get_or_create(
                username=login_field,
                defaults={"email": email, "is_active": True},
            )
        if email and user.email != email:
            user.email = email
            user.save(update_fields=["email"])
        osimart_customer_id = osimart_data.get("customer", {}).get("id") or osimart_data.get("id")
        if osimart_customer_id:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.osimart_customer_id = str(osimart_customer_id)
            profile.save(update_fields=["osimart_customer_id"])
        login(request, user)
        resp_data = _user_data(user)
        resp_data["osimart_token"] = access_token
        resp_data["osimart_refresh_token"] = osimart_data.get("refresh_token", "")
        return Response(resp_data)

    # Osimart auth failed — clean up orphaned local user if one exists
    try:
        orphan = User.objects.filter(
            Q(username=login_field) | Q(email=login_field),
            is_staff=False,
        ).first()
        if orphan:
            logger.info("Deleting orphaned local user %s (%s) — no longer on Osimart", orphan.username, orphan.email)
            orphan.delete()
    except Exception:
        pass
    return Response({"error": "Invalid email or password."}, status=401)


@api_view(['POST'])
@permission_classes([AllowAny])
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
@permission_classes([IsAuthenticated, IsStaffOrAdminOnly])
def admin_order_list(request):
    orders = Order.objects.all().prefetch_related("items").order_by("-created_at")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsStaffOrAdminOnly])
def admin_order_update_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=404)
    new_status = request.data.get("status")
    if new_status not in dict(Order.Status.choices):
        return Response({"error": f"Invalid status. Choices: {dict(Order.Status.choices)}"}, status=400)
    order.status = new_status
    order.save(update_fields=["status"])
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
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

    payment_intent_id = data.get("payment_intent_id", "")

    if settings.STRIPE_SECRET_KEY:
        if not payment_intent_id:
            return Response({"error": "Payment is required."}, status=400)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if intent.status != "succeeded":
                return Response({"error": f"Payment not confirmed (status: {intent.status})."}, status=400)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=400)

    gift_card_code = data.get("gift_card_code", "")
    gift_card_discount = data.get("gift_card_discount")

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        email=email,
        name=name,
        address=address,
        gift_card_code=gift_card_code,
        gift_card_discount=gift_card_discount,
        payment_intent_id=payment_intent_id,
        payment_status="paid" if payment_intent_id else "pending",
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
# Orders
# ---------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=404)
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def order_tracking(request, pk):
    try:
        order = Order.objects.get(pk=pk)
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


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def back_in_stock_subscribe(request):
    from .serializers import BackInStockSerializer
    from .models import BackInStockRequest
    serializer = BackInStockSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error": "Invalid request.", "details": serializer.errors}, status=400)
    slug = serializer.validated_data["product_slug"]
    email = serializer.validated_data["email"]
    product_name = serializer.validated_data.get("product_name", "")
    _, created = BackInStockRequest.objects.get_or_create(
        product_slug=slug, email=email,
        defaults={"product_name": product_name},
    )
    if created:
        return Response({"message": "We'll notify you when this product is back in stock!"}, status=201)
    return Response({"message": "You're already subscribed for this product."})

@api_view(['GET'])
@permission_classes([AllowAny])
def api_version(request):
    return Response({"version": "1.0.0", "api": "techstore"})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def newsletter_subscribe(request):
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


# ---------------------------------------------------------------------------
# Stripe Payments
# ---------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def payment_config(request):
    return Response({
        "publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        "mode": "live" if settings.STRIPE_SECRET_KEY else "demo",
    })


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def create_payment_intent(request):
    amount = request.data.get("amount")
    if not amount:
        return Response({"error": "Amount is required."}, status=400)

    if not settings.STRIPE_SECRET_KEY:
        return Response({
            "client_secret": None,
            "mode": "demo",
            "message": "Demo mode — no real payment will be processed.",
        })

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(round(float(amount) * 100)),
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
        return Response({
            "client_secret": intent.client_secret,
            "mode": "live",
        })
    except stripe.error.StripeError as e:
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def confirm_payment(request):
    payment_intent_id = request.data.get("payment_intent_id")
    if not payment_intent_id:
        return Response({"error": "Payment intent ID is required."}, status=400)

    if not settings.STRIPE_SECRET_KEY:
        return Response({
            "status": "succeeded",
            "mode": "demo",
        })

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return Response({
            "status": intent.status,
            "mode": "live",
        })
    except stripe.error.StripeError as e:
        return Response({"error": str(e)}, status=400)
