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

    def load_all(self, verbosity=0):
        self._load_categories(verbosity)
        self._load_brands(verbosity)
        self._load_variant_types(verbosity)
        self._load_collections(verbosity)
        self._load_products(verbosity)

    def _items(self, subdir):
        d = os.path.join(self.data_dir, subdir)
        if not os.path.isdir(d):
            return
        for fname in sorted(os.listdir(d)):
            if fname.endswith(".json"):
                with open(os.path.join(d, fname)) as f:
                    yield fname, json.load(f)

    def _load_categories(self, verbosity):
        for fname, data in self._items("categories"):
            try:
                result = self.client.create_category(data)
                self.category_map[data["name"]] = result.get("id")
                if verbosity >= 1:
                    print(f"  ✓ Category '{data['name']}'")
            except OsimartError as e:
                print(f"  ✗ {fname}: {e}")

    def _load_brands(self, verbosity):
        for fname, data in self._items("brands"):
            try:
                result = self.client.create_brand(data)
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
                if "category" in payload and payload["category"] in self.category_map:
                    payload["category_id"] = self.category_map[payload.pop("category")]
                if "brand" in payload and payload["brand"] in self.brand_map:
                    payload["brand_id"] = self.brand_map[payload.pop("brand")]
                if "collections" in payload:
                    payload["collection_ids"] = [
                        self.collection_map[c]
                        for c in payload.pop("collections", [])
                        if c in self.collection_map
                    ]
                result = self.client.create_product(payload)
                if verbosity >= 1:
                    print(f"  ✓ Product '{data['name']}'")
            except OsimartError as e:
                print(f"  ✗ {fname}: {e}")
