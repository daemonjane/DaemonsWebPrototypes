from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from .models import Cart, CartItem, Category, Order, Product, Wishlist


class ImportVueDataTests(TestCase):
    def test_creates_products_and_categories(self):
        self.assertEqual(Product.objects.count(), 0)
        out = StringIO()
        call_command("import_vue_data", stdout=out)
        self.assertEqual(Product.objects.count(), 21)
        self.assertIn("21 products", out.getvalue())
        self.assertIn("21 created", out.getvalue())
        cats = set(Category.objects.values_list("slug", flat=True))
        self.assertIn("desktop", cats)
        self.assertIn("monitors", cats)
        self.assertIn("peripherals", cats)

    def test_updates_existing_products(self):
        cat = Category.objects.create(slug="peripherals", name="Peripherals")
        Product.objects.create(
            slug="cyberpro-keyboard",
            name="Old Name",
            price="50",
            category=cat,
            rating=0.0,
        )
        out = StringIO()
        call_command("import_vue_data", stdout=out)
        keyboard = Product.objects.get(slug="cyberpro-keyboard")
        self.assertEqual(keyboard.name, "Cyber-Pro Mechanical Keyboard")
        self.assertIn("21 products", out.getvalue())
        self.assertIn("20 created, 1 updated", out.getvalue())

    def test_idempotent(self):
        call_command("import_vue_data", stdout=StringIO())
        first = Product.objects.count()
        call_command("import_vue_data", stdout=StringIO())
        self.assertEqual(Product.objects.count(), first)


class AuthAPITests(TestCase):
    def test_register_success(self):
        resp = self.client.post("/api/auth/register/", {"username": "newuser", "email": "new@example.com", "password": "Pass123!"}, content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["username"], "newuser")
        self.assertEqual(data["email"], "new@example.com")
        self.assertFalse(data["is_staff"])
        self.assertIn("profile", data)

    def test_register_duplicate_username(self):
        self.client.post("/api/auth/register/", {"username": "dup", "email": "a@example.com", "password": "Pass123!"}, content_type="application/json")
        resp = self.client.post("/api/auth/register/", {"username": "dup", "email": "b@example.com", "password": "Pass123!"}, content_type="application/json")
        self.assertEqual(resp.status_code, 409)

    def test_register_duplicate_email(self):
        self.client.post("/api/auth/register/", {"username": "user1", "email": "same@example.com", "password": "Pass123!"}, content_type="application/json")
        resp = self.client.post("/api/auth/register/", {"username": "user2", "email": "same@example.com", "password": "Pass123!"}, content_type="application/json")
        self.assertEqual(resp.status_code, 409)

    def test_register_missing_fields(self):
        resp = self.client.post("/api/auth/register/", {"username": "", "email": "", "password": ""}, content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_login_success(self):
        self.client.post("/api/auth/register/", {"username": "loginuser", "email": "login@example.com", "password": "Pass123!"}, content_type="application/json")
        resp = self.client.post("/api/auth/login/", {"username": "loginuser", "password": "Pass123!"}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["username"], "loginuser")

    def test_login_bad_password(self):
        resp = self.client.post("/api/auth/login/", {"username": "nonexistent", "password": "wrong"}, content_type="application/json")
        self.assertEqual(resp.status_code, 401)

    def test_profile_requires_auth(self):
        resp = self.client.get("/api/auth/profile/")
        self.assertEqual(resp.status_code, 401)

    def test_profile_authenticated(self):
        self.client.post("/api/auth/register/", {"username": "prouser", "email": "pro@example.com", "password": "Pass123!"}, content_type="application/json")
        resp = self.client.get("/api/auth/profile/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["username"], "prouser")

    def test_profile_update(self):
        self.client.post("/api/auth/register/", {"username": "upduser", "email": "upd@example.com", "password": "Pass123!"}, content_type="application/json")
        resp = self.client.patch("/api/auth/profile/", {"bio": "Hello world", "location": "NYC", "phone": "+123"}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        profile = resp.json()["profile"]
        self.assertEqual(profile["bio"], "Hello world")
        self.assertEqual(profile["location"], "NYC")
        self.assertEqual(profile["phone"], "+123")

    def test_logout(self):
        self.client.post("/api/auth/register/", {"username": "logoutuser", "email": "lo@example.com", "password": "Pass123!"}, content_type="application/json")
        resp = self.client.post("/api/auth/logout/")
        self.assertEqual(resp.status_code, 200)
        resp2 = self.client.get("/api/auth/profile/")
        self.assertEqual(resp2.status_code, 401)


def _login(client):
    client.post("/api/auth/register/", {"username": "testuser", "email": "test@example.com", "password": "Pass123!"}, content_type="application/json")


def _seed_product():
    cat = Category.objects.get_or_create(slug="peripherals", name="Peripherals")[0]
    return Product.objects.get_or_create(
        slug="test-product",
        defaults={"name": "Test Product", "price": "99.99", "category": cat, "rating": 4.5, "image": "/assets/test.jpg"},
    )[0]


class CartAPITests(TestCase):
    def test_cart_requires_auth(self):
        resp = self.client.get("/api/cart/")
        self.assertEqual(resp.status_code, 401)

    def test_cart_get_creates_empty_cart(self):
        _login(self.client)
        resp = self.client.get("/api/cart/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["items"], [])
        self.assertEqual(resp.json()["total_items"], 0)

    def test_cart_add_product(self):
        _login(self.client)
        _seed_product()
        resp = self.client.post("/api/cart/add/", {"product_slug": "test-product", "quantity": 2}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total_items"], 2)
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["name"], "Test Product")

    def test_cart_add_increments_quantity(self):
        _login(self.client)
        _seed_product()
        self.client.post("/api/cart/add/", {"product_slug": "test-product", "quantity": 1}, content_type="application/json")
        resp = self.client.post("/api/cart/add/", {"product_slug": "test-product", "quantity": 3}, content_type="application/json")
        self.assertEqual(resp.json()["items"][0]["quantity"], 4)

    def test_cart_add_invalid_product(self):
        _login(self.client)
        resp = self.client.post("/api/cart/add/", {"product_slug": "nonexistent"}, content_type="application/json")
        self.assertEqual(resp.status_code, 404)

    def test_cart_add_upgrade(self):
        _login(self.client)
        resp = self.client.post("/api/cart/add/", {"name": "VIP Build", "price": 99.99, "item_type": "upgrade"}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["items"][0]["item_type"], "upgrade")

    def test_cart_update_quantity(self):
        _login(self.client)
        _seed_product()
        add = self.client.post("/api/cart/add/", {"product_slug": "test-product", "quantity": 1}, content_type="application/json")
        item_id = add.json()["items"][0]["id"]
        resp = self.client.patch(f"/api/cart/item/{item_id}/", {"quantity": 5}, content_type="application/json")
        self.assertEqual(resp.json()["items"][0]["quantity"], 5)

    def test_cart_remove_item(self):
        _login(self.client)
        _seed_product()
        add = self.client.post("/api/cart/add/", {"product_slug": "test-product", "quantity": 1}, content_type="application/json")
        item_id = add.json()["items"][0]["id"]
        resp = self.client.delete(f"/api/cart/item/{item_id}/")
        self.assertEqual(resp.json()["items"], [])

    def test_cart_clear(self):
        _login(self.client)
        _seed_product()
        self.client.post("/api/cart/add/", {"product_slug": "test-product", "quantity": 2}, content_type="application/json")
        resp = self.client.post("/api/cart/clear/")
        self.assertEqual(resp.json()["items"], [])

    def test_cart_merge(self):
        _login(self.client)
        _seed_product()
        resp = self.client.post("/api/cart/merge/", {"items": [{"id": "test-product", "name": "Test Product", "price": 99.99, "quantity": 3}]}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["total_items"], 3)


class WishlistAPITests(TestCase):
    def test_wishlist_requires_auth(self):
        resp = self.client.get("/api/wishlist/")
        self.assertEqual(resp.status_code, 401)

    def test_wishlist_toggle_add(self):
        _login(self.client)
        _seed_product()
        resp = self.client.post("/api/wishlist/toggle/", {"slug": "test-product"}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["added"])
        self.assertIn("test-product", resp.json()["product_slugs"])

    def test_wishlist_toggle_remove(self):
        _login(self.client)
        _seed_product()
        self.client.post("/api/wishlist/toggle/", {"slug": "test-product"}, content_type="application/json")
        resp = self.client.post("/api/wishlist/toggle/", {"slug": "test-product"}, content_type="application/json")
        self.assertFalse(resp.json()["added"])
        self.assertNotIn("test-product", resp.json()["product_slugs"])

    def test_wishlist_check_favorite(self):
        _login(self.client)
        _seed_product()
        self.client.post("/api/wishlist/toggle/", {"slug": "test-product"}, content_type="application/json")
        resp = self.client.get("/api/wishlist/check/test-product/")
        self.assertTrue(resp.json()["is_favorite"])

    def test_wishlist_check_not_favorite(self):
        _login(self.client)
        _seed_product()
        resp = self.client.get("/api/wishlist/check/test-product/")
        self.assertFalse(resp.json()["is_favorite"])

    def test_wishlist_get(self):
        _login(self.client)
        _seed_product()
        self.client.post("/api/wishlist/toggle/", {"slug": "test-product"}, content_type="application/json")
        resp = self.client.get("/api/wishlist/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("test-product", resp.json()["product_slugs"])


class OrderAPITests(TestCase):
    def test_order_list_requires_auth(self):
        resp = self.client.get("/api/orders/")
        self.assertEqual(resp.status_code, 403)

    def test_order_checkout_requires_auth(self):
        resp = self.client.post("/api/orders/checkout/", {}, content_type="application/json")
        self.assertEqual(resp.status_code, 401)

    def test_checkout_empty_cart(self):
        _login(self.client)
        resp = self.client.post("/api/orders/checkout/", {"address": "123 Street"}, content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_checkout_success(self):
        _login(self.client)
        _seed_product()
        self.client.post("/api/cart/add/", {"product_slug": "test-product", "quantity": 2}, content_type="application/json")
        resp = self.client.post("/api/orders/checkout/", {"name": "Test User", "email": "test@example.com", "address": "123 Main St"}, content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["status"], "placed")
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["product_slug"], "test-product")
        # Cart should be empty after checkout
        cart_resp = self.client.get("/api/cart/")
        self.assertEqual(cart_resp.json()["items"], [])

    def test_checkout_missing_address(self):
        _login(self.client)
        _seed_product()
        self.client.post("/api/cart/add/", {"product_slug": "test-product", "quantity": 1}, content_type="application/json")
        resp = self.client.post("/api/orders/checkout/", {}, content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_order_list(self):
        _login(self.client)
        _seed_product()
        self.client.post("/api/cart/add/", {"product_slug": "test-product", "quantity": 1}, content_type="application/json")
        self.client.post("/api/orders/checkout/", {"address": "123 Main St"}, content_type="application/json")
        resp = self.client.get("/api/orders/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

    def test_order_detail(self):
        _login(self.client)
        _seed_product()
        self.client.post("/api/cart/add/", {"product_slug": "test-product", "quantity": 1}, content_type="application/json")
        checkout = self.client.post("/api/orders/checkout/", {"address": "123 Main St"}, content_type="application/json")
        order_id = checkout.json()["id"]
        resp = self.client.get(f"/api/orders/{order_id}/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["id"], order_id)


class SearchAPITests(TestCase):
    def setUp(self):
        call_command("import_vue_data", verbosity=0)

    def test_search_returns_results(self):
        resp = self.client.get("/api/products/search/?q=keyboard")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreater(data["count"], 0)
        self.assertTrue(any("Keyboard" in p["name"] for p in data["results"]))

    def test_search_no_query(self):
        resp = self.client.get("/api/products/search/")
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(resp.json()["count"], 0)

    def test_search_no_results(self):
        resp = self.client.get("/api/products/search/?q=zzzznotexist")
        self.assertEqual(resp.json()["count"], 0)

    def test_search_by_category(self):
        resp = self.client.get("/api/products/search/?category=desktop")
        self.assertEqual(resp.status_code, 200)
        for p in resp.json()["results"]:
            self.assertEqual(p["category_slug"], "desktop")
