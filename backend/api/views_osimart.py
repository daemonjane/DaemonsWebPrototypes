import logging
import uuid

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from services.osimart import OsimartClient, OsimartError

logger = logging.getLogger(__name__)


def _simplify_main_image(out):
    if "main_image" not in out:
        return
    img = out["main_image"]
    out["main_image"] = img.get("id", "") if isinstance(img, dict) else img

def _simplify_gallery(out):
    if "gallery" not in out or not isinstance(out["gallery"], list):
        return
    simplified = []
    for g in out["gallery"]:
        if not isinstance(g, dict):
            simplified.append(g)
            continue
        entry = dict(g)
        media = entry.get("media", {})
        entry["media"] = media.get("id", "") if isinstance(media, dict) else media
        simplified.append(entry)
    out["gallery"] = simplified

def _simplify_product(p):
    """Osimart GET returns expanded nested objects, but PUT expects simplified formats."""
    out = dict(p)
    out.pop("id", None)
    _simplify_main_image(out)
    _simplify_gallery(out)
    _simplify_categories(out)
    _simplify_variants(out)
    _simplify_brand(out)
    _simplify_quantity_unit(out)
    _simplify_id_lists(out)
    return out

def _simplify_categories(out):
    if "categories" not in out or not isinstance(out["categories"], list):
        return
    simplified = []
    for c in out["categories"]:
        cat = c.get("category", {})
        cat_id = cat.get("id", "") if isinstance(cat, dict) else cat
        simplified.append({"category": cat_id})
    out["categories"] = simplified

def _simplify_variants(out):
    if "variants" not in out or not isinstance(out["variants"], list):
        return
    simplified = []
    for v in out["variants"]:
        v_out = dict(v)
        v_out.pop("id", None)
        v_out.pop("product", None)
        v_out.pop("fulfillment_locations", None)
        if "resources" in v_out and isinstance(v_out["resources"], list):
            v_out["resources"] = [r.get("id", "") if isinstance(r, dict) else r for r in v_out["resources"]]
        simplified.append(v_out)
    out["variants"] = simplified

def _simplify_brand(out):
    if "brand" not in out or not isinstance(out["brand"], dict):
        return
    out["brand"] = out["brand"].get("id", "")

def _simplify_quantity_unit(out):
    if "quantity_unit" not in out or not isinstance(out["quantity_unit"], dict):
        return
    out["quantity_unit"] = out["quantity_unit"].get("id", "")

def _simplify_id_lists(out):
    for key in ["collections", "resources", "sections", "catalogs"]:
        if key in out and isinstance(out[key], list):
            try:
                out[key] = [item.get("id", "") if isinstance(item, dict) else item for item in out[key]]
            except (TypeError, AttributeError):
                pass


def osimart_api_view(methods):
    """Like @api_view but csrf_exempt + no auth — for osimart proxy views."""
    def decorator(func):
        func = permission_classes([AllowAny])(func)
        func = authentication_classes([])(func)
        func = api_view(methods)(func)
        func.csrf_exempt = True
        return func
    return decorator


def _get_client():
    return OsimartClient()


def _resolve_product_id(client, product_id):
    """If product_id is not a UUID, look it up by slugified_name."""
    if _validate_uuid(product_id):
        return product_id
    try:
        products = client.get_products(params={"limit": 100})
        results = products.get("results", [])
        for p in results:
            if p.get("slugified_name") == product_id:
                return p["id"]
    except Exception:
        pass
    return product_id


def _proxy_get(method_name, request, cache_seconds=60, *args):
    try:
        client = _get_client()
        params = request.GET.dict()
        method = getattr(client, method_name)
        data = method(*args, params=params)
        resp = Response(data)
        resp["Cache-Control"] = f"public, max-age={cache_seconds}"
        return resp
    except OsimartError as e:
        err = {"error": str(e)}
        if e.response_body:
            err["detail"] = e.response_body
        status = e.status_code if isinstance(e.status_code, int) else 502
        return Response(err, status=status)
    except Exception as e:
        logger.exception("Unhandled error in _proxy_get(%s)", method_name)
        return Response({"error": str(e), "detail": f"Unhandled error: {e}"}, status=502)


def _proxy_write(method_name, *args):
    try:
        client = _get_client()
        method = getattr(client, method_name)
        data = method(*args)
        return Response(data)
    except OsimartError as e:
        err = {"error": str(e)}
        if e.response_body:
            err["detail"] = e.response_body
        status = e.status_code if isinstance(e.status_code, int) else 502
        return Response(err, status=status)
    except Exception as e:
        logger.exception("Unhandled error in _proxy_write(%s)", method_name)
        return Response({"error": str(e), "detail": f"Unhandled error: {e}"}, status=502)


# ---------------------------------------------------------------------------
# Banners
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_banners(request):
    if request.method == "GET":
        return _proxy_get("get_banners", request)
    return _proxy_write("create_banner", request.data)


@osimart_api_view(["GET", "PUT", "DELETE"])
def osimart_banner_detail(request, banner_id):
    if request.method == "GET":
        return _proxy_get("get_banner", request, 0, banner_id)
    if request.method == "DELETE":
        return _proxy_write("delete_banner", banner_id)
    return _proxy_write("update_banner", banner_id, request.data)


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_products(request):
    if request.method == "GET":
        return _proxy_get("get_products", request)
    return _proxy_write("create_product", request.data)


@osimart_api_view(["GET", "PUT", "PATCH", "DELETE"])
def osimart_product_detail(request, product_id):
    if request.method == "GET":
        client = _get_client()
        resolved = _resolve_product_id(client, product_id)
        return _proxy_get("get_product", request, 0, resolved)
    if request.method == "DELETE":
        return _proxy_write("delete_product", product_id)
    client = _get_client()
    resolved = _resolve_product_id(client, product_id)
    try:
        existing = client.get_product(resolved)
    except OsimartError:
        existing = {}
    merged = _simplify_product(existing)
    merged.update(request.data)
    merged.setdefault("store", client.store_id)
    return _proxy_write("update_product", resolved, merged)


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_categories(request):
    if request.method == "GET":
        return _proxy_get("get_categories", request)
    return _proxy_write("create_category", request.data)


@osimart_api_view(["GET", "PUT", "PATCH", "DELETE"])
def osimart_category_detail(request, category_id):
    if request.method == "GET":
        return _proxy_get("get_category", request, 0, category_id)
    if request.method == "DELETE":
        return _proxy_write("delete_category", category_id)
    return _proxy_write("update_category", category_id, request.data)


# ---------------------------------------------------------------------------
# Brands
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_brands(request):
    if request.method == "GET":
        return _proxy_get("get_brands", request)
    return _proxy_write("create_brand", request.data)


@osimart_api_view(["GET", "PUT", "PATCH", "DELETE"])
def osimart_brand_detail(request, brand_id):
    if request.method == "GET":
        return _proxy_get("get_brand", request, 0, brand_id)
    if request.method == "DELETE":
        return _proxy_write("delete_brand", brand_id)
    return _proxy_write("update_brand", brand_id, request.data)


# ---------------------------------------------------------------------------
# Collections
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_collections(request):
    if request.method == "GET":
        return _proxy_get("get_collections", request)
    return _proxy_write("create_collection", request.data)


@osimart_api_view(["GET", "PUT", "PATCH", "DELETE"])
def osimart_collection_detail(request, collection_id):
    if request.method == "GET":
        return _proxy_get("get_collection", request, 0, collection_id)
    if request.method == "DELETE":
        return _proxy_write("delete_collection", collection_id)
    return _proxy_write("update_collection", collection_id, request.data)


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "PUT"])
def osimart_store(request):
    if request.method == "GET":
        return _proxy_get("get_store", request)
    return _proxy_write("update_store", request.data)


# ---------------------------------------------------------------------------
# Home (dashboard data)
# ---------------------------------------------------------------------------
@osimart_api_view(["GET"])
def osimart_home(request):
    return _proxy_get("get_home", request)


# ---------------------------------------------------------------------------
# Quantity units
# ---------------------------------------------------------------------------
@osimart_api_view(["GET"])
def osimart_quantity_units(request):
    return _proxy_get("get_quantity_units", request)


# ---------------------------------------------------------------------------
# Variant types
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_variant_types(request):
    if request.method == "GET":
        return _proxy_get("get_variant_types", request)
    return _proxy_write("create_variant_type", request.data)


@osimart_api_view(["GET", "PUT", "PATCH", "DELETE"])
def osimart_variant_type_detail(request, vt_id):
    if request.method == "GET":
        return _proxy_get("get_variant_type", request, 0, vt_id)
    if request.method == "DELETE":
        return _proxy_write("delete_variant_type", vt_id)
    return _proxy_write("update_variant_type", vt_id, request.data)


# ---------------------------------------------------------------------------
# Announcement bars
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_announcement_bars(request):
    if request.method == "GET":
        return _proxy_get("get_announcement_bars", request)
    return _proxy_write("create_announcement_bar", request.data)


@osimart_api_view(["GET", "PUT", "PATCH", "DELETE"])
def osimart_announcement_bar_detail(request, ann_id):
    if request.method == "GET":
        return _proxy_get("get_announcement_bar", request, 0, ann_id)
    if request.method == "DELETE":
        return _proxy_write("delete_announcement_bar", ann_id)
    return _proxy_write("update_announcement_bar", ann_id, request.data)


# ---------------------------------------------------------------------------
# Customers
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_customers(request):
    if request.method == "GET":
        return _proxy_get("get_customers", request)
    return _proxy_write("create_customer", request.data)


@osimart_api_view(["GET", "PUT", "PATCH", "DELETE"])
def osimart_customer_detail(request, customer_id):
    if request.method == "GET":
        return _proxy_get("get_customer", request, 0, customer_id)
    if request.method == "DELETE":
        return _proxy_write("delete_customer", customer_id)
    return _proxy_write("update_customer", customer_id, request.data)


# ---------------------------------------------------------------------------
# Media
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_medias(request):
    if request.method == "GET":
        return _proxy_get("get_medias", request)
    return _proxy_write("create_media", request.data)


@osimart_api_view(["GET", "DELETE"])
def osimart_media_detail(request, media_id):
    if request.method == "GET":
        return _proxy_get("get_media", request, 0, media_id)
    return _proxy_write("delete_media", media_id)


# ---------------------------------------------------------------------------
# Shipping zones
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_shipping_zones(request):
    if request.method == "GET":
        return _proxy_get("get_shipping_zones", request)
    return _proxy_write("create_shipping_zone", request.data)


@osimart_api_view(["GET", "PUT", "PATCH", "DELETE"])
def osimart_shipping_zone_detail(request, zone_id):
    if request.method == "GET":
        return _proxy_get("get_shipping_zone", request, 0, zone_id)
    if request.method == "DELETE":
        return _proxy_write("delete_shipping_zone", zone_id)
    return _proxy_write("update_shipping_zone", zone_id, request.data)


# ---------------------------------------------------------------------------
# Order status choices (status definitions)
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_order_status_choices(request):
    if request.method == "GET":
        return _proxy_get("get_order_status_choices", request)
    return _proxy_write("create_order_status_choice", request.data)


@osimart_api_view(["GET", "PUT", "PATCH", "DELETE"])
def osimart_order_status_choice_detail(request, status_id):
    if request.method == "GET":
        return _proxy_get("get_order_status_choice", request, 0, status_id)
    if request.method == "DELETE":
        return _proxy_write("delete_order_status_choice", status_id)
    return _proxy_write("update_order_status_choice", status_id, request.data)


# ---------------------------------------------------------------------------
# Osimart Cart (store-level APIs)
# ---------------------------------------------------------------------------
@csrf_exempt
@require_GET
def osimart_cart_view(request):
    try:
        client = _get_client()
        data = client.get_cart()
        return JsonResponse(data, safe=False)
    except OsimartError as e:
        return JsonResponse({"error": str(e)}, status=502)


@csrf_exempt
@require_POST
def osimart_cart_update_item(request):
    import json
    try:
        body = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    try:
        client = _get_client()
        item_id = body.get("item_id")
        action = body.get("action")
        if not item_id or not action:
            return JsonResponse({"error": "item_id and action are required."}, status=400)
        data = client.update_cart_item(item_id, action, body)
        return JsonResponse(data, safe=False)
    except OsimartError as e:
        return JsonResponse({"error": str(e)}, status=502)

def _validate_uuid(value):
    """Return True if value is a valid UUID string."""
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, TypeError, AttributeError):
        return False
