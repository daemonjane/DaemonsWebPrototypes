"""
Management command to import products from src/data/products.js into Osimart.
"""
import json
import os
import re

import requests
from django.core.management.base import BaseCommand

BASE = os.environ.get("OSIMART_API_BASE_URL", "https://api.osimart.com")
STORE = os.environ.get("OSIMART_STORE_ID", "")
EMAIL = os.environ.get("OSIMART_EMAIL", "")
PASSWORD = os.environ.get("OSIMART_PASSWORD", "")

CATEGORY_MAP = {
    "desktop": "db7b5f82-b06f-49fa-a6ac-567beb56f4f1",
    "monitors": "7dcdc3ce-a7ab-4c6a-a18a-c81fca839d8b",
    "peripherals": "49349baf-6108-4385-b9a7-54fd098a4452",
    "accessories": "6a9592e4-527a-401c-ac6e-115e05ba379a",
    "furniture": "6ccee918-1e12-4a98-ac36-26a3eb5854a2",
    "components": "f3d39fe9-b874-4bf6-8371-b345889dd494",
}

PRODUCTS_JS_PATH = "src/data/products.js"


def parse_products_js(path):
    """Parse the Vue products.js file and return a list of product dicts."""
    with open(path) as f:
        content = f.read()

    # Strip export and outer array
    content = re.sub(r'^export const \w+\s*=\s*', '', content)
    content = content.rstrip().rstrip(';')

    # Replace JS single-quote strings with JSON double-quote strings
    # This is a simplified parser — handles our known data shape

    products = []
    # Match each top-level object in the array
    pattern = re.compile(r'\{\s*id:\s*\'([^\']+)\'(.*?)\},?\s*(?=\{|$)', re.DOTALL)

    pos = 0
    while True:
        # Find next opening brace at top level
        brace_start = content.find('{', pos)
        if brace_start == -1:
            break

        depth = 0
        in_string = False
        i = brace_start
        while i < len(content):
            ch = content[i]
            if ch == "'" and (i == 0 or content[i - 1] != '\\'):
                in_string = not in_string
            elif not in_string:
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        obj_str = content[brace_start:i + 1]
                        product = _parse_product_obj(obj_str)
                        if product:
                            products.append(product)
                        pos = i + 1
                        break
            i += 1
        else:
            break

    return products


def _parse_product_obj(obj_str):
    """Convert a JS object literal string to a Python dict."""
    product = {}
    # Extract key-value pairs using regex
    pairs = re.findall(
        r"""(\w+)\s*:\s*(?:'((?:[^'\\]|\\.)*)'|(\d+(?:\.\d+)?)|null|(\[[^\]]+\])|(\{[^}]+\}))""",
        obj_str,
    )
    for key, str_val, num_val, arr_val, obj_val in pairs:
        if str_val is not None:
            product[key] = str_val
        elif num_val is not None:
            product[key] = float(num_val) if '.' in num_val else int(num_val)
        elif arr_val is not None:
            product[key] = arr_val
        elif obj_val is not None:
            product[key] = obj_val
        else:
            product[key] = None

    # Manually extract features and specs since regex is imprecise
    features_match = re.search(r"features:\s*\[(.+?)\]", obj_str, re.DOTALL)
    if features_match:
        features = re.findall(r"'((?:[^'\\]|\\.)*)'", features_match.group(1))
        product["features"] = features

    specs_match = re.search(r"specs:\s*\{(.+?)\}", obj_str, re.DOTALL)
    if specs_match:
        specs = {}
        spec_pairs = re.findall(r"(\w+):\s*'((?:[^'\\]|\\.)*)'", specs_match.group(1))
        for k, v in spec_pairs:
            specs[k] = v
        product["specs"] = specs

    # Extract category
    cat_match = re.search(r"category:\s*'([^']+)'", obj_str)
    if cat_match:
        product["category"] = cat_match.group(1)

    return product


def build_description(product):
    """Build an HTML description from product data."""
    parts = [f"<p>{product.get('description', '')}</p>"]

    features = product.get("features", [])
    if features:
        parts.append("<ul>")
        for f in features:
            parts.append(f"<li>{f}</li>")
        parts.append("</ul>")

    specs = product.get("specs", {})
    if specs:
        parts.append("<table>")
        for k, v in specs.items():
            parts.append(f"<tr><td><strong>{k.replace('_', ' ').title()}</strong></td><td>{v}</td></tr>")
        parts.append("</table>")

    return "\n".join(parts)


class Command(BaseCommand):
    help = "Import all 21 products from products.js into the Osimart platform."

    def handle(self, *args, **options):
        if not all([STORE, EMAIL, PASSWORD]):
            self.stderr.write("Missing OSIMART env vars (STORE, EMAIL, PASSWORD)")
            return

        products = parse_products_js(PRODUCTS_JS_PATH)
        self.stdout.write(f"Parsed {len(products)} products from {PRODUCTS_JS_PATH}")

        if not products:
            self.stderr.write("No products parsed — check the parser")
            return

        # Login
        sess = requests.Session()
        r = sess.post(f"{BASE}/auth/login/", json={"email": EMAIL, "password": PASSWORD})
        if r.status_code != 200:
            self.stderr.write(f"Login failed: {r.status_code} {r.text[:200]}")
            return
        access = r.json().get("access_token") or r.json().get("token")
        headers = {"Authorization": f"Bearer {access}", "Content-Type": "application/json"}

        created = 0
        skipped = 0
        errors = []

        for product in products:
            pid = product.get("id", "unknown")
            name = product.get("name", pid)
            cat = product.get("category", "")
            cat_uuid = CATEGORY_MAP.get(cat)

            if not cat_uuid:
                self.stdout.write(f"  SKIP {name}: unknown category '{cat}'")
                skipped += 1
                continue

            # Check if product already exists by name
            r = sess.get(
                f"{BASE}/dashboard/apis/products/",
                params={"store": STORE, "search": name, "limit": 1},
                headers=headers,
            )
            existing = r.json()
            if existing.get("count", 0) > 0:
                self.stdout.write(f"  SKIP {name}: already exists")
                skipped += 1
                continue

            # Create media (placeholder image)
            price = product.get("price", 0)
            img_url = (
                f"https://placehold.co/600x400/1e293b/38bdf8?"
                f"text={requests.utils.quote(name.replace(' ', '+'))}"
            )
            r = sess.post(
                f"{BASE}/dashboard/apis/medias/",
                json={"path": img_url, "store": STORE},
                headers=headers,
            )
            if r.status_code != 201:
                self.stderr.write(f"  ERROR {name}: media creation failed {r.status_code}")
                errors.append(name)
                continue
            media_id = r.json()["id"]

            # Build product payload
            payload = {
                "name": name,
                "description": build_description(product),
                "variants": [{"price": float(price), "stock": 50}],
                "categories": [{"category": cat_uuid}],
                "main_image": media_id,
                "gallery": [{"media": media_id}],
                "store": STORE,
            }

            r = sess.post(
                f"{BASE}/dashboard/apis/products/",
                json=payload,
                headers=headers,
            )
            if r.status_code == 201:
                self.stdout.write(f"  OK   {name} (${price})")
                created += 1
            else:
                self.stderr.write(f"  ERROR {name}: {r.status_code} {r.text[:200]}")
                errors.append(name)

        self.stdout.write(f"\nDone. Created: {created}, Skipped: {skipped}, Errors: {len(errors)}")
        if errors:
            self.stderr.write(f"Errors: {', '.join(errors)}")
