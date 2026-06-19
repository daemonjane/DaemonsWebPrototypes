from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

page_patterns = [
    path("shop/", views.page_placeholder, {"page_name": "shop"}, name="shop"),
    path("favorites/", views.page_placeholder, {"page_name": "favorites"}, name="favorites"),
    path("insights/", views.page_placeholder, {"page_name": "insights"}, name="insights"),
    path("about/", views.page_placeholder, {"page_name": "about"}, name="about"),
    path("faq/", views.page_placeholder, {"page_name": "faq"}, name="faq"),
    path("privacy/", views.page_placeholder, {"page_name": "privacy"}, name="privacy"),
    path("terms/", views.page_placeholder, {"page_name": "terms"}, name="terms"),
    path("cookies/", views.page_placeholder, {"page_name": "cookies"}, name="cookies"),
]

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("humans.txt", views.humans_txt, name="humans_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
    path("contact/", views.contact, name="contact"),
    path("accounts/register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="website/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/search/", views.task_search, name="task_search"),
    path("tasks/create/", views.task_create, name="task_create"),
    path("tasks/<int:pk>/", views.task_detail, name="task_detail"),
    path("tasks/<int:pk>/toggle/", views.task_toggle, name="task_toggle"),
    path("tasks/<int:pk>/edit/", views.task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),
] + page_patterns
