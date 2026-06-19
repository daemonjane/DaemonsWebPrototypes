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
    path("contact/", views.contact, name="contact"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/create/", views.task_create, name="task_create"),
] + page_patterns
