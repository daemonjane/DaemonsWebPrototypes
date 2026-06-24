from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from .models import Category, Product


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
