"""Osimart API client for product and order integration."""
import os
import time

import requests


class OsimartError(Exception):
    pass


class OsimartClient:
    BASE_URL = os.environ.get("OSIMART_API_BASE_URL", "https://api.osimart.com")
    STORE_ID = os.environ.get("OSIMART_STORE_ID", "")
    EMAIL = os.environ.get("OSIMART_EMAIL", "")
    PASSWORD = os.environ.get("OSIMART_PASSWORD", "")

    _access_token = None
    _refresh_token = None
    _token_expires_at = 0

    def __init__(self, store_id=None, timeout=15):
        """Initialize Osimart API client with optional store override and request timeout."""
        self.store_id = store_id or self.STORE_ID
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------
    def _ensure_token(self):
        if self._access_token and time.time() < self._token_expires_at - 60:
            return
        if self._refresh_token:
            try:
                self._refresh()
                return
            except OsimartError:
                pass
        self._login()

    def _login(self):
        url = f"{self.BASE_URL}/auth/login/"
        resp = requests.post(url, json={
            "email": self.EMAIL,
            "password": self.PASSWORD,
        }, timeout=self.timeout)
        if resp.status_code != 200:
            raise OsimartError(f"Login failed: {resp.status_code} {resp.text[:200]}")
        data = resp.json()
        self._access_token = data["access_token"]
        self._refresh_token = data.get("refresh_token")
        self._token_expires_at = time.time() + 3600

    def _refresh(self):
        url = f"{self.BASE_URL}/auth/refresh/"
        resp = requests.post(url, json={
            "refresh_token": self._refresh_token,
        }, timeout=self.timeout)
        if resp.status_code != 200:
            raise OsimartError(f"Token refresh failed: {resp.status_code}")
        data = resp.json()
        self._access_token = data.get("access_token", data.get("token"))
        self._token_expires_at = time.time() + 3600

    def _get_headers(self):
        self._ensure_token()
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }

    # ------------------------------------------------------------------
    # Internal HTTP helpers
    # ------------------------------------------------------------------
    def _api_url(self, path):
        return f"{self.BASE_URL}/dashboard/apis/{path.lstrip('/')}"

    def _get(self, path, params=None):
        url = self._api_url(path)
        params = dict(params or {})
        params.setdefault("store", self.store_id)
        try:
            resp = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            if resp.status_code == 401:
                self._access_token = None
                resp = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise OsimartError(f"Osimart API error: {e}") from e

    def _post(self, path, data=None):
        url = self._api_url(path)
        payload = dict(data or {})
        payload.setdefault("store", self.store_id)
        try:
            resp = requests.post(url, json=payload, headers=self._get_headers(), timeout=self.timeout)
            if resp.status_code == 401:
                self._access_token = None
                resp = requests.post(url, json=payload, headers=self._get_headers(), timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise OsimartError(f"Osimart API error: {e}") from e

    # ------------------------------------------------------------------
    # Image helpers
    # ------------------------------------------------------------------
    def image_url(self, path):
        if not path:
            return None
        if path.startswith("http"):
            return path
        return f"{self.BASE_URL}/{path.lstrip('/')}"

    # ------------------------------------------------------------------
    # Resource methods
    # ------------------------------------------------------------------
    def get_banners(self, params=None):
        return self._get("banners/", params)

    def get_products(self, params=None):
        return self._get("products/", params)

    def get_product(self, product_id, params=None):
        return self._get(f"products/{product_id}/", params)

    def get_categories(self, params=None):
        return self._get("categories/", params)

    def get_brands(self, params=None):
        return self._get("brands/", params)

    def get_collections(self, params=None):
        return self._get("collections/", params)

    def get_store(self, store_id=None, params=None):
        sid = store_id or self.store_id
        return self._get(f"stores/{sid}/", params)

    def create_media(self, image_url):
        return self._post("medias/", {"path": image_url})

    def create_product(self, data):
        return self._post("products/", data)

    def get_home(self, params=None):
        url = self._api_url("home/")
        params = dict(params or {})
        params.setdefault("store_id", self.store_id)
        try:
            resp = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            if resp.status_code == 401:
                self._access_token = None
                resp = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise OsimartError(f"Osimart API error: {e}") from e

    def get_quantity_units(self, params=None):
        return self._get("quantity-units/", params)

    def get_variant_types(self, params=None):
        return self._get("variant-types/", params)
