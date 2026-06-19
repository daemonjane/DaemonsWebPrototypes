from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import Task

PAGES = {
    "shop": ("Shop", "Browse our curated collection of premium hardware."),
    "favorites": ("Favorites", "Your saved wishlist items."),
    "insights": ("Market Pulse", "Real-time market insights and trends."),
    "about": ("About", "Learn more about TechStore and our mission."),
    "faq": ("FAQ", "Frequently asked questions."),
    "privacy": ("Privacy Policy", "How we handle your data."),
    "terms": ("Terms of Service", "Terms governing your use of TechStore."),
    "cookies": ("Cookie Policy", "How we use cookies."),
}


def home(request):
    recent_tasks = Task.objects.all()[:5]
    return render(request, "website/home.html", {"recent_tasks": recent_tasks})


def page_placeholder(request, page_name):
    title, description = PAGES.get(page_name, ("Page", "This page is coming soon."))
    return render(request, "website/page_placeholder.html", {"title": title, "description": description})


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


def custom_404(request, exception):
    return render(request, "website/404.html", status=404)


def custom_500(request):
    return render(request, "website/500.html", status=500)
