"""Integration tests for API views — cart, wishlist, orders, auth, addons."""

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model


def _login(client):
    user = get_user_model().objects.create_user(
        username="testuser", email="test@example.com", password="Pass123!"
    )
    from website.models import UserProfile
    UserProfile.objects.create(user=user)
    client.force_login(user)


@override_settings(DEBUG=True)
class AuthAPITests(TestCase):
    def test_register_success(self):
        resp = self.client.post("/api/auth/register/", {"username": "newuser", "email": "new@example.com", "password": "Pass123!"}, content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["status"], "pending")
        self.assertEqual(data["email"], "new@example.com")

    def test_register_duplicate_username(self):
        get_user_model().objects.create_user(username="dup", email="a@example.com", password="Pass123!")
        resp = self.client.post("/api/auth/register/", {"username": "dup", "email": "b@example.com", "password": "Pass123!"}, content_type="application/json")
        self.assertEqual(resp.status_code, 409)

    def test_register_duplicate_email(self):
        get_user_model().objects.create_user(username="user1", email="same@example.com", password="Pass123!")
        resp = self.client.post("/api/auth/register/", {"username": "user2", "email": "same@example.com", "password": "Pass123!"}, content_type="application/json")
        self.assertEqual(resp.status_code, 409)

    def test_register_missing_fields(self):
        resp = self.client.post("/api/auth/register/", {"username": "", "email": "", "password": ""}, content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_staff_login_success(self):
        user = get_user_model().objects.create_user(username="loginuser", email="login@example.com", password="Pass123!", is_staff=True)
        from website.models import UserProfile
        UserProfile.objects.create(user=user)
        resp = self.client.post("/api/auth/staff-login/", {"username": "loginuser", "password": "Pass123!"}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["username"], "loginuser")

    def test_staff_login_bad_password(self):
        resp = self.client.post("/api/auth/staff-login/", {"username": "nonexistent", "password": "wrong"}, content_type="application/json")
        self.assertEqual(resp.status_code, 401)

    def test_profile_requires_auth(self):
        resp = self.client.get("/api/auth/profile/")
        self.assertEqual(resp.status_code, 401)

    def test_profile_authenticated(self):
        user = get_user_model().objects.create_user(username="prouser", email="pro@example.com", password="Pass123!")
        from website.models import UserProfile
        UserProfile.objects.create(user=user)
        self.client.force_login(user)
        resp = self.client.get("/api/auth/profile/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["username"], "prouser")

    def test_profile_update(self):
        user = get_user_model().objects.create_user(username="upduser", email="upd@example.com", password="Pass123!")
        from website.models import UserProfile
        UserProfile.objects.create(user=user)
        self.client.force_login(user)
        resp = self.client.patch("/api/auth/profile/", {"bio": "Hello world", "location": "NYC", "phone": "+123"}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        profile = resp.json()["profile"]
        self.assertEqual(profile["bio"], "Hello world")
        self.assertEqual(profile["location"], "NYC")
        self.assertEqual(profile["phone"], "+123")

    def test_logout(self):
        user = get_user_model().objects.create_user(username="logoutuser", email="lo@example.com", password="Pass123!")
        from website.models import UserProfile
        UserProfile.objects.create(user=user)
        self.client.force_login(user)
        resp = self.client.post("/api/auth/logout/")
        self.assertEqual(resp.status_code, 200)
        resp2 = self.client.get("/api/auth/profile/")
        self.assertEqual(resp2.status_code, 401)


@override_settings(DEBUG=True)
class OsimartCartAPITests(TestCase):
    def test_cart_view_requires_auth(self):
        resp = self.client.get("/api/osimart/cart/view/")
        self.assertEqual(resp.status_code, 401)

    def test_cart_update_item_requires_auth(self):
        resp = self.client.post("/api/osimart/cart/update-item/", {}, content_type="application/json")
        self.assertEqual(resp.status_code, 401)


@override_settings(DEBUG=True)
class WishlistAPITests(TestCase):
    def test_wishlist_requires_auth(self):
        resp = self.client.get("/api/wishlist/")
        self.assertEqual(resp.status_code, 401)

    def test_wishlist_toggle_add(self):
        _login(self.client)
        resp = self.client.post("/api/wishlist/toggle/", {"slug": "test-product"}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["added"])
        self.assertIn("test-product", resp.json()["product_slugs"])

    def test_wishlist_toggle_remove(self):
        _login(self.client)
        self.client.post("/api/wishlist/toggle/", {"slug": "test-product"}, content_type="application/json")
        resp = self.client.post("/api/wishlist/toggle/", {"slug": "test-product"}, content_type="application/json")
        self.assertFalse(resp.json()["added"])
        self.assertNotIn("test-product", resp.json()["product_slugs"])

    def test_wishlist_check_favorite(self):
        _login(self.client)
        self.client.post("/api/wishlist/toggle/", {"slug": "test-product"}, content_type="application/json")
        resp = self.client.get("/api/wishlist/check/test-product/")
        self.assertTrue(resp.json()["is_favorite"])

    def test_wishlist_check_not_favorite(self):
        _login(self.client)
        resp = self.client.get("/api/wishlist/check/test-product/")
        self.assertFalse(resp.json()["is_favorite"])

    def test_wishlist_get(self):
        _login(self.client)
        self.client.post("/api/wishlist/toggle/", {"slug": "test-product"}, content_type="application/json")
        resp = self.client.get("/api/wishlist/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("test-product", resp.json()["product_slugs"])


@override_settings(DEBUG=True)
class OrderAPITests(TestCase):
    def test_order_list_requires_auth(self):
        resp = self.client.get("/api/orders/")
        self.assertEqual(resp.status_code, 403)

    def test_checkout_missing_required_fields(self):
        resp = self.client.post("/api/orders/checkout/", {}, content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_checkout_empty_cart(self):
        _login(self.client)
        resp = self.client.post("/api/orders/checkout/", {"name": "Test User", "email": "test@example.com", "address": "123 Street"}, content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_checkout_success(self):
        _login(self.client)
        resp = self.client.post("/api/orders/checkout/", {
            "name": "Test User",
            "email": "test@example.com",
            "address": "123 Main St",
            "items": [{"name": "Test Product", "price": 99.99, "quantity": 2}],
        }, content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["status"], "placed")
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["name"], "Test Product")

    def test_checkout_missing_address(self):
        _login(self.client)
        resp = self.client.post("/api/orders/checkout/", {
            "name": "Test User",
            "email": "test@example.com",
            "items": [{"name": "Test Product", "price": 99.99, "quantity": 1}],
        }, content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_order_list(self):
        _login(self.client)
        self.client.post("/api/orders/checkout/", {
            "name": "Test User",
            "email": "test@example.com",
            "address": "123 Main St",
            "items": [{"name": "Test Product", "price": 99.99, "quantity": 1}],
        }, content_type="application/json")
        resp = self.client.get("/api/orders/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

    def test_order_detail(self):
        _login(self.client)
        checkout = self.client.post("/api/orders/checkout/", {
            "name": "Test User",
            "email": "test@example.com",
            "address": "123 Main St",
            "items": [{"name": "Test Product", "price": 99.99, "quantity": 1}],
        }, content_type="application/json")
        order_id = checkout.json()["id"]
        resp = self.client.get(f"/api/orders/{order_id}/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["id"], order_id)



