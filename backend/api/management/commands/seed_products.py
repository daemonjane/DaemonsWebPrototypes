"""Fast product seeding — creates products from seed_data JSON on Osimart."""
import json
import os
import time
import requests
from django.core.management.base import BaseCommand

BASE = os.environ.get("OSIMART_API_BASE_URL", "https://api.osimart.com")
STORE = os.environ.get("OSIMART_STORE_ID", "")
EMAIL = os.environ.get("OSIMART_EMAIL", "")
PASSWORD = os.environ.get("OSIMART_PASSWORD", "")

SEED_DIR = os.path.join(os.path.dirname(__file__), "seed_data", "products")


def login():
    r = requests.post(f"{BASE}/auth/login/", json={"email": EMAIL, "password": PASSWORD}, timeout=15)
    r.raise_for_status()
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def get_existing_product_names(headers):
    names = set()
    page = 1
    while True:
        r = requests.get(f"{BASE}/dashboard/apis/products/", params={"store": STORE, "limit": 100, "page": page}, headers=headers, timeout=15)
        r.raise_for_status()
        data = r.json()
        for p in (data.get("results") or []):
            names.add(p["name"].strip().lower())
        if not data.get("next"):
            break
        page += 1
    return names


def resolve_category_map(headers):
    """Build a name→id map from existing Osimart categories."""
    mapping = {}
    r = requests.get(f"{BASE}/dashboard/apis/categories/", params={"store": STORE, "limit": 500}, headers=headers, timeout=15)
    r.raise_for_status()
    data = r.json()
    items = data if isinstance(data, list) else data.get("results", [])
    for c in items:
        name = (c.get("name") or "").strip().lower()
        slug = (c.get("slugified_name") or "").strip().lower()
        if name and name not in mapping:
            mapping[name] = c["id"]
        if slug and slug not in mapping:
            mapping[slug] = c["id"]
    return mapping


def resolve_brand_map(headers):
    mapping = {}
    r = requests.get(f"{BASE}/dashboard/apis/brands/", params={"store": STORE, "limit": 500}, headers=headers, timeout=15)
    r.raise_for_status()
    data = r.json()
    items = data if isinstance(data, list) else data.get("results", [])
    for b in items:
        name = (b.get("name") or "").strip().lower()
        slug = (b.get("slugified_name") or "").strip().lower()
        if name and name not in mapping:
            mapping[name] = b["id"]
        if slug and slug not in mapping:
            mapping[slug] = b["id"]
    return mapping


def resolve_media(url, headers):
    """Upload image URL and return media UUID."""
    if not url:
        return None
    try:
        r = requests.post(f"{BASE}/dashboard/apis/medias/", json={"path": url, "store": STORE}, headers=headers, timeout=15)
        if r.status_code == 201:
            return r.json()["id"]
    except Exception:
        pass
    return None


class Command(BaseCommand):
    help = "Seed 51 products from seed_data JSON files into Osimart store."

    def handle(self, *args, **options):
        if not all([STORE, EMAIL, PASSWORD]):
            self.stderr.write("Missing OSIMART env vars")
            return

        verbosity = int(options["verbosity"])
        headers = login()
        self.stdout.write("Logged in to Osimart API")

        existing = get_existing_product_names(headers)
        self.stdout.write(f"Existing products: {len(existing)}")

        cat_map = resolve_category_map(headers)
        brand_map = resolve_brand_map(headers)
        self.stdout.write(f"Resolved {len(cat_map)} categories, {len(brand_map)} brands")

        if not os.path.isdir(SEED_DIR):
            self.stderr.write(f"Seed directory not found: {SEED_DIR}")
            return

        created = 0
        skipped = 0
        errors = []

        for fname in sorted(os.listdir(SEED_DIR)):
            if not fname.endswith(".json"):
                continue

            path = os.path.join(SEED_DIR, fname)
            with open(path) as f:
                data = json.load(f)

            name = data.get("name", "").strip()
            if not name:
                continue
            if name.lower() in existing:
                self.stdout.write(f"  SKIP (exists) {name}")
                skipped += 1
                continue

            payload = {
                "store": STORE,
                "name": name,
                "description": data.get("description", ""),
                "price_range": str(data.get("price_range", "0")),
            }

            # Category
            cat_name = (data.get("category") or "").strip().lower()
            if cat_name in cat_map:
                payload["category_id"] = cat_map[cat_name]
                payload["categories"] = [{"category": cat_map[cat_name]}]

            # Brand
            brand_name = (data.get("brand") or "").strip().lower()
            if brand_name in brand_map:
                payload["brand_id"] = brand_map[brand_name]

            # Images — upload main_image, build gallery
            main_img = data.get("main_image") or ""
            if main_img:
                mid = resolve_media(main_img, headers)
                if mid:
                    payload["main_image"] = mid
                    payload["gallery"] = [{"media": mid}]
                    time.sleep(0.3)

            # Variant
            stock = data.get("stock", data.get("remaining_stock", 50))
            payload["variants"] = [{
                "name": "Default",
                "price": str(data.get("price_range", "0")),
                "remaining_stock": stock,
            }]

            # Collections
            collections = data.get("collections", [])
            payload["collections"] = collections

            try:
                r = requests.post(f"{BASE}/dashboard/apis/products/", json=payload, headers=headers, timeout=30)
                if r.status_code == 201:
                    self.stdout.write(f"  OK   {name}")
                    created += 1
                    existing.add(name.lower())
                else:
                    self.stderr.write(f"  FAIL {name}: {r.status_code} {r.text[:150]}")
                    errors.append(name)
            except Exception as e:
                self.stderr.write(f"  ERROR {name}: {e}")
                errors.append(name)

            time.sleep(0.2)

        self.stdout.write(f"\nDone. Created: {created}, Skipped: {skipped}, Errors: {len(errors)}")
