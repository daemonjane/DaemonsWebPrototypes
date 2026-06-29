from django.views.decorators.cache import cache_page

from rest_framework.decorators import api_view
from rest_framework.response import Response

from services.osimart import OsimartClient, OsimartError


def _get_client():
    return OsimartClient()


def _proxy(request, method_name, cache_seconds=60, *args, **kwargs):
    try:
        client = _get_client()
        params = request.GET.dict()
        method = getattr(client, method_name)
        data = method(*args, **kwargs, params=params)
        response = Response(data)
        response["Cache-Control"] = f"public, max-age={cache_seconds}"
        return response
    except OsimartError as e:
        return Response({"error": str(e)}, status=502)


@api_view(["GET"])
def osimart_banners(request):
    return _proxy(request, "get_banners")


@api_view(["GET"])
def osimart_products(request):
    return _proxy(request, "get_products")


@api_view(["GET"])
def osimart_product_detail(request, product_id):
    return _proxy(request, "get_product", product_id)


@api_view(["GET"])
def osimart_categories(request):
    return _proxy(request, "get_categories")


@api_view(["GET"])
def osimart_store(request):
    return _proxy(request, "get_store")


@api_view(["GET"])
def osimart_home(request):
    return _proxy(request, "get_home")


@api_view(["GET"])
def osimart_brands(request):
    return _proxy(request, "get_brands")


@api_view(["GET"])
def osimart_collections(request):
    return _proxy(request, "get_collections")


@api_view(["GET"])
def osimart_quantity_units(request):
    return _proxy(request, "get_quantity_units")


@api_view(["GET"])
def osimart_variant_types(request):
    return _proxy(request, "get_variant_types")
