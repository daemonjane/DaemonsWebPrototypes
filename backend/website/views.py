from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string


def vue_spa(request):
    """Serve the built Vue SPA (dist/index.html)."""
    spa_path = Path(settings.BASE_DIR.parent) / "dist" / "index.html"
    if not spa_path.exists():
        return HttpResponse("Vue app not built. Run `npm run build` in the project root.", status=200)
    with open(spa_path) as f:
        return HttpResponse(f.read(), content_type="text/html; charset=utf-8")


from .email_utils import send_contact_auto_reply, send_subscription_confirmation
from .forms import CommentForm, ContactForm, RegisterForm, TaskForm
from .models import Comment, ContactMessage, NewsletterSubscription, Task

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
    """Serve the Vue SPA homepage."""
    return vue_spa(request)


@staff_member_required
def admin_dashboard(request):
    from datetime import timedelta
    from decimal import Decimal

    from django.db.models import Count, Sum, F
    from django.db.models.functions import TruncDate
    from django.utils import timezone

    from api.models import Category, Order, OrderItem, Product, Wishlist

    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    fourteen_days_ago = now - timedelta(days=14)

    product_count = Product.objects.count()
    category_count = Category.objects.count()
    order_count = Order.objects.count()
    task_count = Task.objects.count()
    comment_count = Comment.objects.count()
    contact_count = ContactMessage.objects.count()
    user_count = User.objects.count()
    wishlist_count = Wishlist.objects.count()

    total_revenue = OrderItem.objects.aggregate(
        total=Sum(F("price") * F("quantity"))
    )["total"] or Decimal("0.00")

    orders_by_status = {
        s: Order.objects.filter(status=s).count()
        for s, _ in Order.Status.choices
    }

    products_by_category = list(
        Category.objects.annotate(count=Count("products"))
        .values("name", "count")
        .order_by("-count")
    )

    daily_orders = list(
        Order.objects.filter(created_at__gte=fourteen_days_ago)
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )

    daily_revenue = list(
        OrderItem.objects.filter(order__created_at__gte=thirty_days_ago)
        .annotate(date=TruncDate("order__created_at"))
        .values("date")
        .annotate(total=Sum(F("price") * F("quantity")))
        .order_by("date")
    )

    top_products = list(
        OrderItem.objects.filter(product__isnull=False)
        .values(name=F("product__name"), slug=F("product__slug"))
        .annotate(total_qty=Sum("quantity"), total_rev=Sum(F("price") * F("quantity")))
        .order_by("-total_qty")[:10]
    )

    task_done = Task.objects.filter(completed=True).count()
    task_pending = task_count - task_done

    order_status_labels = [s[1] for s in Order.Status.choices]
    order_status_data = [orders_by_status.get(s[0], 0) for s in Order.Status.choices]

    cat_labels = [c["name"] for c in products_by_category]
    cat_data = [c["count"] for c in products_by_category]

    do_labels = [d["date"].strftime("%b %d") for d in daily_orders]
    do_data = [d["count"] for d in daily_orders]

    dr_labels = [d["date"].strftime("%b %d") for d in daily_revenue]
    dr_data = [float(d["total"]) for d in daily_revenue]

    tp_labels = [p["name"] for p in top_products]
    tp_qty = [p["total_qty"] for p in top_products]
    tp_rev = [float(p["total_rev"]) for p in top_products]

    recent_orders = Order.objects.select_related().order_by("-created_at")[:5]
    recent_tasks = Task.objects.prefetch_related("comments").order_by("-created_at")[:5]

    return render(request, "website/admin_dashboard.html", {
        "product_count": product_count,
        "category_count": category_count,
        "order_count": order_count,
        "task_count": task_count,
        "comment_count": comment_count,
        "contact_count": contact_count,
        "user_count": user_count,
        "wishlist_count": wishlist_count,
        "total_revenue": float(total_revenue),
        "order_status_labels": order_status_labels,
        "order_status_data": order_status_data,
        "cat_labels": cat_labels,
        "cat_data": cat_data,
        "do_labels": do_labels,
        "do_data": do_data,
        "dr_labels": dr_labels,
        "dr_data": dr_data,
        "tp_labels": tp_labels,
        "tp_qty": tp_qty,
        "tp_rev": tp_rev,
        "task_done": task_done,
        "task_pending": task_pending,
        "recent_orders": recent_orders,
        "recent_tasks": recent_tasks,
    })


def sitemap_xml(request):
    static_urls = [
        "/", "/tasks/", "/contact/", "/shop/", "/about/", "/faq/", "/privacy/", "/terms/", "/cookies/",
    ]
    task_urls = [f"/tasks/{t.pk}/" for t in Task.objects.all()]
    product_urls = []
    try:
        from services.osimart import OsimartClient
        client = OsimartClient()
        data = client.get_products()
        for p in data.get("results", []):
            slug = p.get("slugified_name", "")
            if slug:
                product_urls.append(f"/product/{slug}/")
    except Exception:
        pass
    all_urls = static_urls + task_urls + product_urls
    entries = "".join(f"<url><loc>{request.build_absolute_uri(url)}</loc></url>" for url in all_urls)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>'
    return HttpResponse(xml, content_type="application/xml")


def page_placeholder(request, page_name):
    """Render a placeholder page for sections not yet built."""
    title, description = PAGES.get(page_name, ("Page", "This page is coming soon."))
    return render(request, "website/page_placeholder.html", {"title": title, "description": description})


def register(request):
    """User registration view with auto-login."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("task_list")
    else:
        form = RegisterForm()
    return render(request, "website/register.html", {"form": form})


def contact(request):
    """Handle contact form GET (display) and POST (validate + save + message)."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            try:
                send_contact_auto_reply(contact_msg)
            except Exception:
                pass
            messages.success(request, "Thank you! Your message has been sent. We will get back to you within 24 hours.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "website/contact.html", {"form": form})


@login_required
def task_list(request):
    """Display paginated tasks in a table with status badges and action icons."""
    task_qs = Task.objects.all()
    task_count = task_qs.count()
    completed_count = task_qs.filter(completed=True).count()

    paginator = Paginator(task_qs, 10)
    page = request.GET.get("page")
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(request, "website/task_list.html", {
        "tasks": tasks,
        "task_count": task_count,
        "completed_count": completed_count,
        "pending_count": task_count - completed_count,
        "page_obj": tasks,
        "paginator": paginator,
    })


@login_required
def task_create(request):
    """Show blank form on GET; validate and save on POST."""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            uploaded = request.FILES.getlist("attachments")
            if len(uploaded) > 4:
                messages.error(request, "You can attach a maximum of 4 files.")
                return render(request, "website/task_form.html", {"form": form, "title": "Create Task"})
            for f in uploaded:
                task.files.create(file=f, name=f.name)
            messages.success(request, "Task created successfully.")
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "website/task_form.html", {"form": form, "title": "Create Task"})


@login_required
def task_update(request, pk):
    """Show prefilled form on GET; validate and save changes on POST."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            uploaded = request.FILES.getlist("attachments")
            if len(uploaded) > 4:
                messages.error(request, "You can attach a maximum of 4 files.")
                return render(request, "website/task_form.html", {"form": form, "title": "Edit Task", "task": task})
            for f in uploaded:
                task.files.create(file=f, name=f.name)
            messages.success(request, "Task updated successfully.")
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "website/task_form.html", {"form": form, "title": "Edit Task", "task": task})


@login_required
def task_toggle(request, pk):
    """Toggle a task's completed status via POST and redirect."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.completed = not task.completed
        task.save()
        status = "completed" if task.completed else "reopened"
        messages.success(request, f"Task '{task.title}' marked as {status}.")
    return redirect("task_list")


@login_required
def task_detail(request, pk):
    """Show a single task's full details with comments."""
    task = get_object_or_404(Task.objects.prefetch_related("files"), pk=pk)
    comments = task.comments.all()
    form = CommentForm()
    return render(request, "website/task_detail.html", {
        "task": task,
        "comments": comments,
        "form": form,
    })


@login_required
def add_comment(request, pk):
    """Handle POST to add a comment to a task."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.save()
            messages.success(request, "Comment added.")
        else:
            messages.error(request, "Please fix the errors below.")
    return redirect("task_detail", pk=pk)


@login_required
def task_delete(request, pk):
    """Show confirmation on GET; delete task + files on POST."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        for tf in task.files.all():
            tf.file.delete(save=False)
        task.delete()
        messages.success(request, f"Task '{task.title}' deleted.")
        return redirect("task_list")
    return render(request, "website/task_confirm_delete.html", {"task": task})


@login_required
def task_search(request):
    """Return JSON of tasks filtered by search query."""
    q = request.GET.get("q", "").strip()
    tasks = Task.objects.filter(title__icontains=q) | Task.objects.filter(description__icontains=q)
    tasks = tasks.distinct().order_by("-created_at")
    data = [
        {
            "pk": t.pk,
            "title": t.title,
            "description": t.description[:80] if t.description else "",
            "completed": t.completed,
            "created": t.created_at.strftime("%b %d"),
            "comment_count": t.comments.count(),
        }
        for t in tasks
    ]
    return JsonResponse({"tasks": data, "count": len(data)})


def newsletter_subscribe(request):
    """Handle newsletter subscription from the footer form."""
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if email:
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email,
                defaults={"active": True},
            )
            if created:
                try:
                    send_subscription_confirmation(subscription)
                except Exception:
                    pass
                messages.success(request, "Thank you for subscribing to our newsletter!")
            else:
                if not subscription.active:
                    subscription.active = True
                    subscription.save()
                    try:
                        send_subscription_confirmation(subscription)
                    except Exception:
                        pass
                    messages.success(request, "Your subscription has been reactivated!")
                else:
                    messages.info(request, "You are already subscribed to our newsletter.")
        else:
            messages.error(request, "Please provide a valid email address.")
    return redirect(request.META.get("HTTP_REFERER", "/"))


def favicon(request):
    return redirect("/favicon.svg")


@login_required
def profile(request):
    return render(request, "website/profile.html", {"profile_user": request.user})


def robots_txt(request):
    return HttpResponse(render_to_string("website/robots.txt", {"request": request}), content_type="text/plain")


def humans_txt(request):
    return HttpResponse(render_to_string("website/humans.txt", {"request": request}), content_type="text/plain")


def bad_request(request, exception=None):
    return render(request, "website/400.html", status=400)


def gone(request, exception=None):
    return render(request, "website/410.html", status=410)


def forbidden(request, exception):
    """Render a themed 403 error page."""
    return render(request, "website/403.html", status=403)


def csrf_failure(request, reason=""):
    """Render a themed 403 page for CSRF failures."""
    return render(request, "website/403_csrf.html", {"reason": reason}, status=403)


def custom_404(request, exception):
    """Render a themed 404 error page."""
    return render(request, "website/404.html", status=404)


def custom_500(request):
    """Render a themed 500 error page."""
    return render(request, "website/500.html", status=500)
