# Context processors for templates.
import random
from datetime import datetime


def site_context(request):
    return {
        "visitor_count": random.randint(120, 180),
        "current_year": datetime.now().year,
        "site_name": "TechStore",
    }
