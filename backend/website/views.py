from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import Task


def home(request):
    recent_tasks = Task.objects.all()[:5]
    return render(request, "website/home.html", {"recent_tasks": recent_tasks})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact_thanks")
    else:
        form = ContactForm()
    return render(request, "website/contact.html", {"form": form})


def contact_thanks(request):
    return render(request, "website/contact_thanks.html")
