from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("humans.txt", views.humans_txt, name="humans_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("contact/", views.contact, name="contact"),
    path("accounts/register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="website/login.html", authentication_form=LoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/search/", views.task_search, name="task_search"),
    path("tasks/create/", views.task_create, name="task_create"),
    path("tasks/<int:pk>/", views.task_detail, name="task_detail"),
    path("tasks/<int:pk>/toggle/", views.task_toggle, name="task_toggle"),
    path("tasks/<int:pk>/edit/", views.task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),
    path("tasks/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("newsletter/", views.newsletter_subscribe, name="newsletter_subscribe"),
    # All unmatched routes serve the Vue SPA (storefront)
    re_path(r"^(?!static/).*$", views.vue_spa, name="vue_spa"),
]
