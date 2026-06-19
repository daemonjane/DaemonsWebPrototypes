from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

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
    """Render the homepage with task stats and recent tasks."""
    tasks = Task.objects.all()
    recent_tasks = tasks[:5]
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    return render(request, "website/home.html", {
        "recent_tasks": recent_tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
    })


def sitemap_xml(request):
    from website.models import Task
    static_urls = [
        "/", "/tasks/", "/contact/", "/shop/", "/about/", "/faq/", "/privacy/", "/terms/", "/cookies/",
    ]
    task_urls = [f"/tasks/{t.pk}/" for t in Task.objects.all()]
    all_urls = static_urls + task_urls
    entries = "".join(f"<url><loc>https://techstore.example.com{url}</loc></url>" for url in all_urls)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>'
    return HttpResponse(xml, content_type="application/xml")


def page_placeholder(request, page_name):
    """Render a placeholder page for sections not yet built."""
    title, description = PAGES.get(page_name, ("Page", "This page is coming soon."))
    return render(request, "website/page_placeholder.html", {"title": title, "description": description})


def contact(request):
    """Handle contact form GET (display) and POST (validate + save + message)."""
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
    """Display all tasks in a table with status badges and action icons."""
    tasks = Task.objects.all()
    task_count = tasks.count()
    completed_count = tasks.filter(completed=True).count()
    return render(request, "website/task_list.html", {
        "tasks": tasks,
        "task_count": task_count,
        "completed_count": completed_count,
        "pending_count": task_count - completed_count,
    })


def task_create(request):
    """Show blank form on GET; validate and save on POST."""
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
    """Show prefilled form on GET; validate and save changes on POST."""
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


def task_toggle(request, pk):
    """Toggle a task's completed status via POST and redirect."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.completed = not task.completed
        task.save()
        status = "completed" if task.completed else "reopened"
        messages.success(request, f"Task '{task.title}' marked as {status}.")
    return redirect("task_list")


def task_detail(request, pk):
    """Show a single task's full details."""
    task = get_object_or_404(Task, pk=pk)
    return render(request, "website/task_detail.html", {"task": task})


def task_delete(request, pk):
    """Show confirmation on GET; delete task on POST."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        messages.success(request, f"Task '{task.title}' deleted.")
        return redirect("task_list")
    return render(request, "website/task_confirm_delete.html", {"task": task})


def robots_txt(request):
    return HttpResponse(render_to_string("website/robots.txt"), content_type="text/plain")


def humans_txt(request):
    return HttpResponse(render_to_string("website/humans.txt"), content_type="text/plain")


def forbidden(request, exception):
    """Render a themed 403 error page."""
    return render(request, "website/403.html", status=403)


def custom_404(request, exception):
    """Render a themed 404 error page."""
    return render(request, "website/404.html", status=404)


def custom_500(request):
    """Render a themed 500 error page."""
    return render(request, "website/500.html", status=500)
