from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from services.osimart import OsimartClient, OsimartError


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
        return Response(err, status=e.status_code)


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
        return Response(err, status=e.status_code)


# ---------------------------------------------------------------------------
# Banners
# ---------------------------------------------------------------------------
@osimart_api_view(["GET"])
def osimart_banners(request):
    return _proxy_get("get_banners", request)


@osimart_api_view(["PUT", "DELETE"])
def osimart_banner_detail(request, banner_id):
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
        return _proxy_get("get_product", request, 0, product_id)
    if request.method == "DELETE":
        return _proxy_write("delete_product", product_id)
    return _proxy_write("update_product", product_id, request.data)


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_categories(request):
    if request.method == "GET":
        return _proxy_get("get_categories", request)
    return _proxy_write("create_category", request.data)


@osimart_api_view(["PUT", "PATCH", "DELETE"])
def osimart_category_detail(request, category_id):
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


@osimart_api_view(["PUT", "PATCH", "DELETE"])
def osimart_brand_detail(request, brand_id):
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


@osimart_api_view(["PUT", "PATCH", "DELETE"])
def osimart_collection_detail(request, collection_id):
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


@osimart_api_view(["PUT", "PATCH", "DELETE"])
def osimart_variant_type_detail(request, vt_id):
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


@osimart_api_view(["PUT", "PATCH", "DELETE"])
def osimart_announcement_bar_detail(request, ann_id):
    if request.method == "DELETE":
        return _proxy_write("delete_announcement_bar", ann_id)
    return _proxy_write("update_announcement_bar", ann_id, request.data)


# ---------------------------------------------------------------------------
# Customers
# ---------------------------------------------------------------------------
@osimart_api_view(["GET"])
def osimart_customers(request):
    return _proxy_get("get_customers", request)


# ---------------------------------------------------------------------------
# Media
# ---------------------------------------------------------------------------
@osimart_api_view(["GET", "POST"])
def osimart_medias(request):
    if request.method == "GET":
        return _proxy_get("get_medias", request)
    return _proxy_write("create_media", request.data)


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
