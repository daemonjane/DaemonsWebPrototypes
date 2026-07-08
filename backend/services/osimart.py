"""Osimart API client for product and order integration."""
import os
import time

import requests


class OsimartError(Exception):
    def __init__(self, message, status_code=502, response_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


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

    def customer_login(self, email, password, device_name="web", device_id=""):
        """Authenticate a customer via the Osimart API and return user data + tokens."""
        url = f"{self.BASE_URL}/auth/login/"
        resp = requests.post(url, json={
            "login_as": "customer",
            "email": email,
            "password": password,
            "device_name": device_name,
            "device_id": device_id,
        }, timeout=self.timeout)
        if resp.status_code != 200:
            raise OsimartError(f"Customer login failed: {resp.status_code} {resp.text[:200]}")
        return resp.json()

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

    def _ensure_store(self, payload=None, params=None):
        payload = dict(payload or {})
        payload.setdefault("store", self.store_id)
        params = dict(params or {})
        params.setdefault("store", self.store_id)
        return payload, params

    def _request(self, method, path, **kwargs):
        url = self._api_url(path)
        try:
            resp = method(url, headers=self._get_headers(), timeout=self.timeout, **kwargs)
            if resp.status_code == 401:
                self._access_token = None
                resp = method(url, headers=self._get_headers(), timeout=self.timeout, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            code = 502
            body = None
            if hasattr(e, 'response') and e.response is not None:
                code = e.response.status_code
                body = e.response.text[:500]
            raise OsimartError(f"Osimart API error: {e}", status_code=code, response_body=body) from e

    def _get(self, path, params=None):
        url = self._api_url(path)
        params, _ = self._ensure_store(params=params)
        try:
            resp = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            if resp.status_code == 401:
                self._access_token = None
                resp = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            code = 502
            body = None
            if hasattr(e, 'response') and e.response is not None:
                code = e.response.status_code
                body = e.response.text[:500]
            raise OsimartError(f"Osimart API error: {e}", status_code=code, response_body=body) from e

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
        except Exception as e:
            code = 502
            body = None
            if hasattr(e, 'response') and e.response is not None:
                code = e.response.status_code
                body = e.response.text[:500]
            raise OsimartError(f"Osimart API error: {e}", status_code=code, response_body=body) from e

    def _put(self, path, data=None):
        url = self._api_url(path)
        payload = dict(data or {})
        payload.setdefault("store", self.store_id)
        try:
            resp = requests.put(url, json=payload, params={"store": self.store_id}, headers=self._get_headers(), timeout=self.timeout)
            if resp.status_code == 401:
                self._access_token = None
                resp = requests.put(url, json=payload, params={"store": self.store_id}, headers=self._get_headers(), timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            code = 502
            body = None
            if hasattr(e, 'response') and e.response is not None:
                code = e.response.status_code
                body = e.response.text[:500]
            raise OsimartError(f"Osimart API error: {e}", status_code=code, response_body=body) from e

    def _patch(self, path, data=None):
        url = self._api_url(path)
        payload = dict(data or {})
        payload.setdefault("store", self.store_id)
        try:
            resp = requests.patch(url, json=payload, params={"store": self.store_id}, headers=self._get_headers(), timeout=self.timeout)
            if resp.status_code == 401:
                self._access_token = None
                resp = requests.patch(url, json=payload, params={"store": self.store_id}, headers=self._get_headers(), timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            code = 502
            body = None
            if hasattr(e, 'response') and e.response is not None:
                code = e.response.status_code
                body = e.response.text[:500]
            raise OsimartError(f"Osimart API error: {e}", status_code=code, response_body=body) from e

    def _delete(self, path):
        url = self._api_url(path)
        try:
            resp = requests.delete(url, headers=self._get_headers(), timeout=self.timeout)
            if resp.status_code == 401:
                self._access_token = None
                resp = requests.delete(url, headers=self._get_headers(), timeout=self.timeout)
            resp.raise_for_status()
            return resp.status_code == 204
        except Exception as e:
            code = 502
            body = None
            if hasattr(e, 'response') and e.response is not None:
                code = e.response.status_code
                body = e.response.text[:500]
            raise OsimartError(f"Osimart API error: {e}", status_code=code, response_body=body) from e

    # ------------------------------------------------------------------
    # Cart (store-level APIs — different base from dashboard)
    # ------------------------------------------------------------------
    def _store_api_url(self, path):
        return f"{self.BASE_URL}/store/apis/{path.lstrip('/')}"

    def get_cart(self, params=None):
        url = self._store_api_url("cart/view")
        params = dict(params or {})
        params.setdefault("store", self.store_id)
        try:
            resp = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            if resp.status_code == 401:
                self._access_token = None
                resp = requests.get(url, params=params, headers=self._get_headers(), timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            code = 502
            body = None
            if hasattr(e, 'response') and e.response is not None:
                code = e.response.status_code
                body = e.response.text[:500]
            raise OsimartError(f"Osimart cart error: {e}", status_code=code, response_body=body) from e

    def update_cart_item(self, item_id, action, data=None):
        url = self._store_api_url("cart/update-item/")
        payload = dict(data or {})
        payload.setdefault("store", self.store_id)
        payload["item_id"] = item_id
        payload["action"] = action
        try:
            resp = requests.post(url, json=payload, headers=self._get_headers(), timeout=self.timeout)
            if resp.status_code == 401:
                self._access_token = None
                resp = requests.post(url, json=payload, headers=self._get_headers(), timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            code = 502
            body = None
            if hasattr(e, 'response') and e.response is not None:
                code = e.response.status_code
                body = e.response.text[:500]
            raise OsimartError(f"Osimart cart error: {e}", status_code=code, response_body=body) from e

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

    def get_banner(self, banner_id):
        return self._get(f"banners/{banner_id}/")

    def get_products(self, params=None):
        return self._get("products/", params)

    def get_product(self, product_id, params=None):
        return self._get(f"products/{product_id}/", params)

    def get_categories(self, params=None):
        return self._get("categories/", params)

    def get_category(self, category_id):
        return self._get(f"categories/{category_id}/")

    def get_brands(self, params=None):
        return self._get("brands/", params)

    def get_brand(self, brand_id):
        return self._get(f"brands/{brand_id}/")

    def get_collections(self, params=None):
        return self._get("collections/", params)

    def get_collection(self, collection_id):
        return self._get(f"collections/{collection_id}/")

    def get_store(self, store_id=None, params=None):
        sid = store_id or self.store_id
        return self._get(f"stores/{sid}/", params)

    def create_media(self, image_url):
        return self._post("medias/", {"path": image_url})

    def create_product(self, data):
        return self._post("products/", data)

    def update_product(self, product_id, data):
        return self._put(f"products/{product_id}/", data)

    def delete_product(self, product_id):
        return self._delete(f"products/{product_id}/")

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
        except Exception as e:
            raise OsimartError(f"Osimart API error: {e}") from e

    def get_quantity_units(self, params=None):
        return self._get("quantity-units/", params)

    def get_variant_types(self, params=None):
        return self._get("variant-types/", params)

    def get_variant_type(self, variant_type_id):
        return self._get(f"variant-types/{variant_type_id}/")

    def create_category(self, data):
        return self._post("categories/", data)

    def update_category(self, category_id, data):
        return self._put(f"categories/{category_id}/", data)

    def delete_category(self, category_id):
        return self._delete(f"categories/{category_id}/")

    def create_brand(self, data):
        return self._post("brands/", data)

    def update_brand(self, brand_id, data):
        return self._put(f"brands/{brand_id}/", data)

    def delete_brand(self, brand_id):
        return self._delete(f"brands/{brand_id}/")

    def create_collection(self, data):
        return self._post("collections/", data)

    def update_collection(self, collection_id, data):
        return self._put(f"collections/{collection_id}/", data)

    def delete_collection(self, collection_id):
        return self._delete(f"collections/{collection_id}/")

    def create_banner(self, data):
        return self._post("banners/", data)

    def update_banner(self, banner_id, data):
        return self._put(f"banners/{banner_id}/", data)

    def delete_banner(self, banner_id):
        return self._delete(f"banners/{banner_id}/")

    def get_announcement_bars(self, params=None):
        return self._get("announcement-bars/", params)

    def create_announcement_bar(self, data):
        return self._post("announcement-bars/", data)

    def update_announcement_bar(self, ann_id, data):
        return self._put(f"announcement-bars/{ann_id}/", data)

    def delete_announcement_bar(self, ann_id):
        return self._delete(f"announcement-bars/{ann_id}/")

    def get_announcement_bar(self, ann_id):
        return self._get(f"announcement-bars/{ann_id}/")

    def get_customers(self, params=None):
        return self._get("customers/", params)

    def get_customer(self, customer_id):
        return self._get(f"customers/{customer_id}/")

    def create_customer(self, data):
        return self._post("customers/", data)

    def update_customer(self, customer_id, data):
        return self._put(f"customers/{customer_id}/", data)

    def delete_customer(self, customer_id):
        return self._delete(f"customers/{customer_id}/")

    def get_medias(self, params=None):
        return self._get("medias/", params)

    def get_media(self, media_id):
        return self._get(f"medias/{media_id}/")

    def create_variant_type(self, data):
        payload = {k: v for k, v in data.items() if k != "values"}
        if "values" in data and data["values"]:
            payload["possible_values"] = data["values"]
        return self._post("variant-types/", payload)

    def update_variant_type(self, vt_id, data):
        payload = {k: v for k, v in data.items() if k != "values"}
        if "values" in data and data["values"]:
            payload["possible_values"] = data["values"]
        return self._put(f"variant-types/{vt_id}/", payload)

    def delete_variant_type(self, vt_id):
        return self._delete(f"variant-types/{vt_id}/")

    def update_store(self, data):
        return self._put(f"stores/{self.store_id}/", data)

    # ------------------------------------------------------------------
    # Shipping zones
    # ------------------------------------------------------------------
    def get_shipping_zones(self, params=None):
        return self._get("shipping-zones/", params)

    def get_shipping_zone(self, zone_id, params=None):
        return self._get(f"shipping-zones/{zone_id}/", params)

    def create_shipping_zone(self, data):
        return self._post("shipping-zones/", data)

    def update_shipping_zone(self, zone_id, data):
        return self._put(f"shipping-zones/{zone_id}/", data)

    def delete_shipping_zone(self, zone_id):
        return self._delete(f"shipping-zones/{zone_id}/")

    # ------------------------------------------------------------------
    # Order status choices (status definitions)
    # ------------------------------------------------------------------
    def get_order_status_choices(self, params=None):
        return self._get("order-status-choices/", params)

    def get_order_status_choice(self, status_id, params=None):
        return self._get(f"order-status-choices/{status_id}/", params)

    def create_order_status_choice(self, data):
        return self._post("order-status-choices/", data)

    def update_order_status_choice(self, status_id, data):
        return self._put(f"order-status-choices/{status_id}/", data)

    def delete_order_status_choice(self, status_id):
        return self._delete(f"order-status-choices/{status_id}/")
