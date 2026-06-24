import os

from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.views.static import serve as static_serve

from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.home, name="home"),
    path("favicon.ico", views.favicon, name="favicon"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("humans.txt", views.humans_txt, name="humans_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("contact/", views.contact, name="contact"),
    path("accounts/register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="website/login.html", authentication_form=LoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/search/", views.task_search, name="task_search"),
    path("tasks/create/", views.task_create, name="task_create"),
    path("tasks/<int:pk>/", views.task_detail, name="task_detail"),
    path("tasks/<int:pk>/toggle/", views.task_toggle, name="task_toggle"),
    path("tasks/<int:pk>/edit/", views.task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),
    path("tasks/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("newsletter/", views.newsletter_subscribe, name="newsletter_subscribe"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT}),
    ]

# Serve the built Vue SPA assets (dist/) at root level in development
if settings.DEBUG:
    dist_root = settings.BASE_DIR.parent / "dist"
    urlpatterns += [
        re_path(r"^assets/(?P<path>.*)$", static_serve, {"document_root": os.path.join(dist_root, "assets")}),
        re_path(r"^(?P<path>favicon\.svg)$", static_serve, {"document_root": dist_root}),
        re_path(r"^(?P<path>icons\.svg)$", static_serve, {"document_root": dist_root}),
    ]

# All unmatched routes serve the Vue SPA (storefront)
urlpatterns += [
    re_path(r"^(?!static/).*$", views.vue_spa, name="vue_spa"),
]
