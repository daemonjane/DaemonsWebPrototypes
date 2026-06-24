"""API URL configuration — Auth, Cart, Orders, Products, Tracking, Add-ons, Osimart."""

from django.urls import path

from . import views
from . import views_osimart

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('auth/register/', views.auth_register, name='auth-register'),
    path('auth/login/', views.auth_login, name='auth-login'),
    path('auth/logout/', views.auth_logout, name='auth-logout'),
    path('auth/profile/', views.auth_profile, name='auth-profile'),
    path('auth/csrf/', views.csrf_token, name='auth-csrf'),
    path('cart/', views.cart_get, name='cart-get'),
    path('cart/add/', views.cart_add, name='cart-add'),
    path('cart/item/<int:item_id>/', views.cart_item_detail, name='cart-item-detail'),
    path('cart/clear/', views.cart_clear, name='cart-clear'),
    path('cart/merge/', views.cart_merge, name='cart-merge'),
    path('wishlist/', views.wishlist_get, name='wishlist-get'),
    path('wishlist/toggle/', views.wishlist_toggle, name='wishlist-toggle'),
    path('wishlist/check/<slug:slug>/', views.wishlist_check, name='wishlist-check'),
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),
    path('orders/<int:pk>/tracking/', views.order_tracking, name='order-tracking'),
    path('orders/checkout/', views.order_checkout, name='order-checkout'),
    path('products/<slug:slug>/addons/', views.product_addons, name='product-addons'),
    path('products/search/', views.product_search, name='product-search'),
    path('version/', views.api_version, name='api-version'),
    path('osimart/banners/', views_osimart.osimart_banners, name='osimart-banners'),
    path('osimart/products/', views_osimart.osimart_products, name='osimart-products'),
    path('osimart/products/<uuid:product_id>/', views_osimart.osimart_product_detail, name='osimart-product-detail'),
    path('osimart/categories/', views_osimart.osimart_categories, name='osimart-categories'),
    path('osimart/store/', views_osimart.osimart_store, name='osimart-store'),
    path('osimart/home/', views_osimart.osimart_home, name='osimart-home'),
    path('osimart/brands/', views_osimart.osimart_brands, name='osimart-brands'),
    path('osimart/collections/', views_osimart.osimart_collections, name='osimart-collections'),
]
