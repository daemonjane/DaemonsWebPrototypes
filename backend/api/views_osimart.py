from rest_framework.decorators import api_view
from rest_framework.response import Response

from services.osimart import OsimartClient, OsimartError


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
        return Response({"error": str(e)}, status=502)


def _proxy_write(method_name, *args):
    try:
        client = _get_client()
        method = getattr(client, method_name)
        data = method(*args)
        return Response(data)
    except OsimartError as e:
        return Response({"error": str(e)}, status=502)


# ---------------------------------------------------------------------------
# Banners
# ---------------------------------------------------------------------------
@api_view(["GET"])
def osimart_banners(request):
    return _proxy_get("get_banners", request)


@api_view(["PUT", "DELETE"])
def osimart_banner_detail(request, banner_id):
    if request.method == "DELETE":
        return _proxy_write("delete_banner", banner_id)
    return _proxy_write("update_banner", banner_id, request.data)


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def osimart_products(request):
    if request.method == "GET":
        return _proxy_get("get_products", request)
    return _proxy_write("create_product", request.data)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def osimart_product_detail(request, product_id):
    if request.method == "GET":
        return _proxy_get("get_product", request, 0, product_id)
    if request.method == "DELETE":
        return _proxy_write("delete_product", product_id)
    return _proxy_write("update_product", product_id, request.data)


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def osimart_categories(request):
    if request.method == "GET":
        return _proxy_get("get_categories", request)
    return _proxy_write("create_category", request.data)


@api_view(["PUT", "PATCH", "DELETE"])
def osimart_category_detail(request, category_id):
    if request.method == "DELETE":
        return _proxy_write("delete_category", category_id)
    return _proxy_write("update_category", category_id, request.data)


# ---------------------------------------------------------------------------
# Brands
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def osimart_brands(request):
    if request.method == "GET":
        return _proxy_get("get_brands", request)
    return _proxy_write("create_brand", request.data)


@api_view(["PUT", "PATCH", "DELETE"])
def osimart_brand_detail(request, brand_id):
    if request.method == "DELETE":
        return _proxy_write("delete_brand", brand_id)
    return _proxy_write("update_brand", brand_id, request.data)


# ---------------------------------------------------------------------------
# Collections
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def osimart_collections(request):
    if request.method == "GET":
        return _proxy_get("get_collections", request)
    return _proxy_write("create_collection", request.data)


@api_view(["PUT", "PATCH", "DELETE"])
def osimart_collection_detail(request, collection_id):
    if request.method == "DELETE":
        return _proxy_write("delete_collection", collection_id)
    return _proxy_write("update_collection", collection_id, request.data)


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------
@api_view(["GET", "PUT"])
def osimart_store(request):
    if request.method == "GET":
        return _proxy_get("get_store", request)
    return _proxy_write("update_store", request.data)


# ---------------------------------------------------------------------------
# Home (dashboard data)
# ---------------------------------------------------------------------------
@api_view(["GET"])
def osimart_home(request):
    return _proxy_get("get_home", request)


# ---------------------------------------------------------------------------
# Quantity units
# ---------------------------------------------------------------------------
@api_view(["GET"])
def osimart_quantity_units(request):
    return _proxy_get("get_quantity_units", request)


# ---------------------------------------------------------------------------
# Variant types
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def osimart_variant_types(request):
    if request.method == "GET":
        return _proxy_get("get_variant_types", request)
    return _proxy_write("create_variant_type", request.data)


@api_view(["PUT", "PATCH", "DELETE"])
def osimart_variant_type_detail(request, vt_id):
    if request.method == "DELETE":
        return _proxy_write("delete_variant_type", vt_id)
    return _proxy_write("update_variant_type", vt_id, request.data)


# ---------------------------------------------------------------------------
# Announcement bars
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def osimart_announcement_bars(request):
    if request.method == "GET":
        return _proxy_get("get_announcement_bars", request)
    return _proxy_write("create_announcement_bar", request.data)


@api_view(["PUT", "PATCH", "DELETE"])
def osimart_announcement_bar_detail(request, ann_id):
    if request.method == "DELETE":
        return _proxy_write("delete_announcement_bar", ann_id)
    return _proxy_write("update_announcement_bar", ann_id, request.data)


# ---------------------------------------------------------------------------
# Customers
# ---------------------------------------------------------------------------
@api_view(["GET"])
def osimart_customers(request):
    return _proxy_get("get_customers", request)


# ---------------------------------------------------------------------------
# Media
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def osimart_medias(request):
    if request.method == "GET":
        return _proxy_get("get_medias", request)
    return _proxy_write("create_media", request.data)
