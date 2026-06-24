import os

import requests


class OsimartError(Exception):
    pass


class OsimartClient:
    """Client for the Osimart external API (banners, products, etc.)."""

    BASE_URL = os.environ.get("OSIMART_API_BASE_URL", "https://api.osimart.com")

    def __init__(self, store_id=None, timeout=15):
        self.store_id = store_id or os.environ.get("OSIMART_STORE_ID", "")
        self.timeout = timeout

    def get_banners(self):
        return self._get("/shop/api/banners/", {"store": self.store_id})

    def _get(self, path, params=None):
        url = f"{self.BASE_URL.rstrip('/')}{path}"
        try:
            resp = requests.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise OsimartError(f"Osimart API error: {e}") from e
