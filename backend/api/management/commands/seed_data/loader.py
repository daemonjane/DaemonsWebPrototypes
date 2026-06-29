"""Seed data loader for populating Osimart catalog from local JSON files."""
import json
import os

from services.osimart import OsimartClient, OsimartError


class SeedLoader:
    def __init__(self, data_dir=None):
        self.data_dir = data_dir or os.path.dirname(__file__)
        self.client = OsimartClient()
        self.category_map = {}
        self.brand_map = {}
        self.vt_map = {}
        self.collection_map = {}
        self._media_cache = {}

    def load_all(self, verbosity=0):
        self._load_categories(verbosity)
        self._load_brands(verbosity)
        self._load_variant_types(verbosity)
        self._load_collections(verbosity)
        self._load_products(verbosity)
        self._load_banners(verbosity)
        self._load_announcements(verbosity)
        self._load_store_settings(verbosity)

    def _items(self, subdir):
        d = os.path.join(self.data_dir, subdir)
        if not os.path.isdir(d):
            return
        for fname in sorted(os.listdir(d)):
            if fname.endswith(".json"):
                with open(os.path.join(d, fname)) as f:
                    yield fname, json.load(f)

    # ------------------------------------------------------------------
    # Media helpers
    # ------------------------------------------------------------------

    def _resolve_media(self, url_or_uuid):
        """Return a media UUID given a URL (upload) or an existing UUID."""
        if not url_or_uuid:
            return None
        val = str(url_or_uuid).strip()
        if val in self._media_cache:
            return self._media_cache[val]
        # Already a UUID (no scheme) — pass through
        if "://" not in val:
            self._media_cache[val] = val
            return val
        # Upload URL → media object
        try:
            result = self.client.create_media(val)
            media_id = result.get("id")
            self._media_cache[val] = media_id
            return media_id
        except OsimartError:
            return None

    def _resolve_media_list(self, urls):
        """Upload a list of image URLs and return list of media UUIDs."""
        return [self._resolve_media(u) for u in (urls or []) if u]

    # ------------------------------------------------------------------
    # Core loaders
    # ------------------------------------------------------------------

    def _load_categories(self, verbosity):
        for fname, data in self._items("categories"):
            try:
                payload = {}
                for key in ("name", "description", "slugified_name", "icon", "parent_category"):
                    if key in data:
                        payload[key] = data[key]
                # Image must be a media UUID or null
                if data.get("image"):
                    payload["image"] = self._resolve_media(data["image"])
                result = self.client.create_category(payload)
                self.category_map[data["name"]] = result.get("id")
                if verbosity >= 1:
                    print(f"  ✓ Category '{data['name']}'")
            except OsimartError as e:
                print(f"  ✗ {fname}: {e}")

    def _load_brands(self, verbosity):
        for fname, data in self._items("brands"):
            try:
                payload = {"name": data["name"]}
                if "slugified_name" in data:
                    payload["slugified_name"] = data["slugified_name"]
                if "website" in data:
                    payload["website"] = data["website"]
                if data.get("logo"):
                    payload["logo"] = self._resolve_media(data["logo"])
                result = self.client.create_brand(payload)
                self.brand_map[data["name"]] = result.get("id")
                if verbosity >= 1:
                    print(f"  ✓ Brand '{data['name']}'")
            except OsimartError as e:
                print(f"  ✗ {fname}: {e}")

    def _load_variant_types(self, verbosity):
        for fname, data in self._items("variant_types"):
            try:
                result = self.client.create_variant_type(data)
                self.vt_map[data["name"]] = result.get("id")
                if verbosity >= 1:
                    print(f"  ✓ Variant '{data['name']}'")
            except OsimartError as e:
                print(f"  ✗ {fname}: {e}")

    def _load_collections(self, verbosity):
        for fname, data in self._items("collections"):
            try:
                result = self.client.create_collection(data)
                self.collection_map[data["name"]] = result.get("id")
                if verbosity >= 1:
                    print(f"  ✓ Collection '{data['name']}'")
            except OsimartError as e:
                print(f"  ✗ {fname}: {e}")

    def _load_products(self, verbosity):
        for fname, data in self._items("products"):
            try:
                payload = dict(data)

                # Resolve name→UUID references
                if "category" in payload and payload["category"] in self.category_map:
                    payload["category_id"] = self.category_map[payload.pop("category")]
                if "brand" in payload and payload["brand"] in self.brand_map:
                    payload["brand_id"] = self.brand_map[payload.pop("brand")]
                if "collections" in payload:
                    payload["collections"] = [
                        self.collection_map[c]
                        for c in payload.pop("collections", [])
                        if c in self.collection_map
                    ]

                # Upload image URLs → media UUIDs
                if payload.get("main_image"):
                    uploaded = self._resolve_media(payload["main_image"])
                    if uploaded:
                        payload["main_image"] = uploaded
                    else:
                        payload.pop("main_image", None)
                if payload.get("images"):
                    uploaded = [u for u in self._resolve_media_list(payload.pop("images")) if u]
                    payload["gallery"] = [{"media": uid} for uid in uploaded]

                # Ensure categories/gallery are lists (API requires them)
                payload.setdefault("categories", [])
                payload.setdefault("gallery", [])
                payload.setdefault("collections", [])

                # Omit sections for now (API does not accept our format)
                payload.pop("sections", None)

                # API expects compare_at_price_range not compare_at_price
                if "compare_at_price" in payload:
                    payload["compare_at_price_range"] = payload.pop("compare_at_price")

                # Map stock field names
                if "remaining_stock" not in payload and "stock" in payload:
                    payload["remaining_stock"] = payload.pop("stock")

                # Ensure at least one variant
                if not payload.get("variants"):
                    default_price = payload.get("price_range", "0")
                    default_stock = payload.get("remaining_stock", 0)
                    payload["variants"] = [{"name": "Default", "price": default_price, "remaining_stock": default_stock}]

                # Ensure price_range is a string
                if "price_range" in payload:
                    payload["price_range"] = str(payload["price_range"])

                result = self.client.create_product(payload)
                if verbosity >= 1:
                    print(f"  ✓ Product '{data['name']}'")
            except OsimartError as e:
                print(f"  ✗ {fname}: {e}")

    def _load_banners(self, verbosity):
        for fname, data in self._items("banners"):
            try:
                payload = {}
                for key in ("title", "subtitle", "label", "active", "display_order",
                            "background_color", "text_color"):
                    if key in data:
                        payload[key] = data[key]

                # API requires fully qualified URL for banner links
                link = data.get("link", "")
                if link:
                    if link.startswith("/"):
                        link = "https://example.com" + link
                    elif not link.startswith("http"):
                        link = "https://example.com/" + link
                payload["link"] = link

                # Upload image as media (required by API)
                if data.get("image"):
                    payload["image"] = self._resolve_media(data["image"])
                if not payload.get("image"):
                    fallback_url = f"https://placehold.co/1920x480?text={data.get('title', 'Banner').replace(' ', '+')}"
                    payload["image"] = self._resolve_media(fallback_url)

                self.client.create_banner(payload)
                if verbosity >= 1:
                    print(f"  ✓ Banner '{data.get('title', fname)}'")
            except OsimartError as e:
                print(f"  ✗ {fname}: {e}")

    def _load_announcements(self, verbosity):
        for fname, data in self._items("announcements"):
            try:
                payload = {
                    "content": data.get("message", data.get("content", "")),
                    "text_color": data.get("text_color", "#000000"),
                }
                for key in ("background_color", "active", "link", "priority", "subtitle"):
                    if key in data:
                        payload[key] = data[key]
                if payload.get("link"):
                    lk = payload["link"]
                    if lk.startswith("/"):
                        payload["link"] = "https://example.com" + lk
                    elif not lk.startswith("http"):
                        payload["link"] = "https://example.com/" + lk
                self.client.create_announcement_bar(payload)
                if verbosity >= 1:
                    print(f"  ✓ Announcement '{payload['content'][:40]}'")
            except OsimartError as e:
                print(f"  ✗ {fname}: {e}")

    def _load_store_settings(self, verbosity):
        store_data = {}
        for fname, data in self._items("store"):
            store_data.update(data)
        if store_data:
            # Only pass fields the API accepts
            allowed = {"name", "primary_color", "secondary_color", "logo"}
            payload = {k: v for k, v in store_data.items() if k in allowed}
            if store_data.get("logo"):
                payload["logo"] = self._resolve_media(store_data["logo"])
            try:
                self.client.update_store(payload)
                if verbosity >= 1:
                    print(f"  ✓ Store settings updated ({len(payload)} fields)")
            except OsimartError as e:
                print(f"  ✗ store settings: {e}")
