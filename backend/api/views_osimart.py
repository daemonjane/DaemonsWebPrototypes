from rest_framework.decorators import api_view
from rest_framework.response import Response

from services.osimart import OsimartClient, OsimartError


@api_view(["GET"])
def osimart_banners(request):
    try:
        client = OsimartClient()
        data = client.get_banners()
        return Response(data)
    except OsimartError as e:
        return Response({"error": str(e)}, status=502)
