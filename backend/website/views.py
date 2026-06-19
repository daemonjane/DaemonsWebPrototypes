from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm, TaskForm
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
            messages.success(request, "Thank you! Your message has been sent. We will get back to you within 24 hours.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "website/contact.html", {"form": form})


def task_list(request):
    tasks = Task.objects.all()
    return render(request, "website/task_list.html", {"tasks": tasks})


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully.")
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "website/task_form.html", {"form": form, "title": "Create Task"})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "website/task_form.html", {"form": form, "title": "Edit Task"})


def custom_404(request, exception):
    return render(request, "website/404.html", status=404)


def custom_500(request):
    return render(request, "website/500.html", status=500)
