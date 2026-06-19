from django.shortcuts import render

from .models import Task


def home(request):
    recent_tasks = Task.objects.all()[:5]
    return render(request, "website/home.html", {"recent_tasks": recent_tasks})
