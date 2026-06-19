import random


def site_context(request):
    return {
        "visitor_count": random.randint(120, 180),
    }
