from django.urls import path

from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('auth/register/', views.auth_register, name='auth-register'),
    path('auth/login/', views.auth_login, name='auth-login'),
    path('auth/logout/', views.auth_logout, name='auth-logout'),
    path('auth/profile/', views.auth_profile, name='auth-profile'),
    path('auth/csrf/', views.csrf_token, name='auth-csrf'),
]
