#!/usr/bin/env python3
"""
Import all 21 products from src/data/products.js into the Osimart platform.

Usage:  python3 import_products.py
(Requires OSIMART_* env vars or .env file in backend/)
"""
import json
import os
import re
import sys

import requests

# --- Config ---
ENV_PATH = "backend/.env"
PRODUCTS_PATH = "src/data/products.js"

# Load .env
if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

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

IMAGE_MAP = {
    "vanguard-desktop":     "vanguard-desktop-fallback.png",
    "ultrawide-monitor":    "ultrawide-monitor-fallback.png",
    "cyberpro-keyboard":    "cyberpro-keyboard-fallback.png",
    "gaming-mouse":         "gamingmouse.jpg",
    "wireless-headset":     "headset.jpg",
    "usb-hub":              "USBhub.jpg",
    "mousepad":             "mousepad.jpg",
    "webcam":               "webcam.webp",
    "speakers":             "speakers.jpg",
    "thermal-paste":        "ThermalCompound2.jpg",
    "cable-ties":           "BraidedCableTies.jpg",
    "cleaning-kit":         "CleaningKit.jpg",
    "gpu-bracket":          "GPU_support_bracket.jpg",
    "displayport-cable":    "DisplayPortCable.jpg",
    "mouse-bungee":         "MouseBungee.webp",
    "stream-deck":          "stream-deck.svg",
    "gaming-chair":         "gaming-chair.svg",
    "cpu-cooler":           "cpu-cooler.svg",
    "nvme-ssd":             "nvme-ssd.svg",
    "sleeved-cables":       "sleeved-cables.svg",
    "microphone":           "microphone.svg",
}

IMG_BASE_URL = "https://cdn.jsdelivr.net/gh/daemonjane/DaemonsWebPrototypes@main/public/assets"

def parse_products(path):
    """Parse products.js and return list of product dicts."""
    with open(path) as f:
        text = f.read()

    products = []
    i = 0
    while i < len(text):
        brace = text.find("{", i)
        if brace == -1:
            break
        depth = 0
        start = brace
        for j in range(brace, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    block = text[start:j+1]
                    p = _parse_block(block)
                    if p:
                        products.append(p)
                    i = j + 1
                    break
        else:
            break
    return products


def _parse_block(block):
    """Extract fields from a single product JS object."""
    p = {}
    p["id"] = _extract_str(block, "id")
    p["name"] = _extract_str(block, "name")
    p["category"] = _extract_str(block, "category")
    p["price"] = _extract_num(block, "price")
    p["description"] = _extract_str(block, "description")
    p["features"] = _extract_str_list(block, "features")
    p["specs"] = _extract_specs(block)
    return p


def _extract_str(text, key):
    m = re.search(rf'\b{key}\s*:\s*\'((?:[^\'\\]|\\.)*)\'', text)
    return m.group(1) if m else None


def _extract_num(text, key):
    m = re.search(rf'\b{key}\s*:\s*(\d+(?:\.\d+)?)', text)
    return float(m.group(1)) if m else 0


def _extract_str_list(text, key):
    m = re.search(rf'\b{key}\s*:\s*\[(.+?)\]', text, re.DOTALL)
    if not m:
        return []
    return re.findall(r"\'((?:[^\'\\]|\\.)*)\'", m.group(1))


def _extract_specs(text):
    m = re.search(r'\bspecs\s*:\s*\{(.+?)\}', text, re.DOTALL)
    if not m:
        return {}
    pairs = re.findall(r"(\w+)\s*:\s*'((?:[^'\\]|\\.)*)'", m.group(1))
    return {k: v for k, v in pairs}


def build_description(p):
    parts = [f"<p>{p.get('description', '')}</p>"]
    features = p.get("features", [])
    if features:
        parts.append("<ul>")
        for f in features:
            parts.append(f"<li>{f}</li>")
        parts.append("</ul>")
    specs = p.get("specs", {})
    if specs:
        parts.append("<table>")
        for k, v in specs.items():
            label = k.replace("_", " ").title()
            parts.append(f"<tr><td><strong>{label}</strong></td><td>{v}</td></tr>")
        parts.append("</table>")
    return "\n".join(parts)


def main():
    if not all([STORE, EMAIL, PASSWORD]):
        sys.exit("Missing OSIMART_* env vars")

    products = parse_products(PRODUCTS_PATH)
    print(f"Parsed {len(products)} products from {PRODUCTS_PATH}\n")

    if not products:
        sys.exit("No products parsed — check the parser")

    sess = requests.Session()
    r = sess.post(f"{BASE}/auth/login/", json={"email": EMAIL, "password": PASSWORD})
    if r.status_code != 200:
        sys.exit(f"Login failed: {r.status_code} {r.text[:200]}")
    access = r.json().get("access_token") or r.json().get("token")
    headers = {"Authorization": f"Bearer {access}", "Content-Type": "application/json"}

    created = 0
    skipped = 0
    errors = []

    for p in products:
        pid = p.get("id", "?")
        name = p.get("name", pid)
        cat = p.get("category", "")
        cat_uuid = CATEGORY_MAP.get(cat)

        if not cat_uuid:
            print(f"  SKIP  {name} — unknown category '{cat}'")
            skipped += 1
            continue

        # Check if exists by name
        r = sess.get(f"{BASE}/dashboard/apis/products/", params={"store": STORE, "search": name, "limit": 1}, headers=headers)
        existing = r.json()
        if existing.get("count", 0) > 0:
            print(f"  SKIP  {name} — already exists")
            skipped += 1
            continue

        # Create media entry from product image asset
        img_file = IMAGE_MAP.get(pid, "")
        img_url = f"{IMG_BASE_URL}/{img_file}" if img_file else ""
        if not img_url:
            print(f"  SKIP  {name} — no image mapping for '{pid}'")
            skipped += 1
            continue
        r = sess.post(f"{BASE}/dashboard/apis/medias/", json={"path": img_url, "store": STORE}, headers=headers)
        if r.status_code != 201:
            print(f"  ERROR {name} — media failed ({r.status_code})")
            errors.append(name)
            continue
        media_id = r.json()["id"]

        payload = {
            "name": name,
            "description": build_description(p),
            "variants": [{"price": float(p.get("price", 0)), "stock": 50}],
            "categories": [{"category": cat_uuid}],
            "main_image": media_id,
            "gallery": [{"media": media_id}],
            "store": STORE,
        }

        r = sess.post(f"{BASE}/dashboard/apis/products/", json=payload, headers=headers)
        if r.status_code == 201:
            print(f"  OK    {name} — ${p.get('price', 0)}")
            created += 1
        else:
            print(f"  ERROR {name} — {r.status_code} {r.text[:200]}")
            errors.append(name)

    print(f"\nDone. Created: {created}, Skipped: {skipped}, Errors: {len(errors)}")
    if errors:
        print(f"Errors: {', '.join(errors)}")


if __name__ == "__main__":
    main()
