"""API URL configuration — Auth, Cart, Orders, Products, Tracking, Add-ons, Osimart."""

from django.urls import path

from . import views
from . import views_osimart

app_name = "api"

# urlpatterns: API URL patterns.
urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('auth/register/', views.auth_register, name='auth-register'),
    path('auth/login/', views.auth_login, name='auth-login'),
    path('auth/logout/', views.auth_logout, name='auth-logout'),
    path('auth/profile/', views.auth_profile, name='auth-profile'),
    path('auth/password-reset/', views.auth_password_reset_request, name='auth-password-reset-request'),
    path('auth/password-reset/<uidb64>/<token>/', views.auth_password_reset_confirm, name='auth-password-reset-confirm'),
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
    path('version/', views.api_version, name='api-version'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='api-newsletter-subscribe'),

    path('osimart/banners/', views_osimart.osimart_banners, name='osimart-banners'),
    path('osimart/banners/<str:banner_id>/', views_osimart.osimart_banner_detail, name='osimart-banner-detail'),
    path('osimart/products/', views_osimart.osimart_products, name='osimart-products'),
    path('osimart/products/<str:product_id>/', views_osimart.osimart_product_detail, name='osimart-product-detail'),
    path('osimart/categories/', views_osimart.osimart_categories, name='osimart-categories'),
    path('osimart/categories/<str:category_id>/', views_osimart.osimart_category_detail, name='osimart-category-detail'),
    path('osimart/store/', views_osimart.osimart_store, name='osimart-store'),
    path('osimart/home/', views_osimart.osimart_home, name='osimart-home'),
    path('osimart/brands/', views_osimart.osimart_brands, name='osimart-brands'),
    path('osimart/brands/<str:brand_id>/', views_osimart.osimart_brand_detail, name='osimart-brand-detail'),
    path('osimart/collections/', views_osimart.osimart_collections, name='osimart-collections'),
    path('osimart/collections/<str:collection_id>/', views_osimart.osimart_collection_detail, name='osimart-collection-detail'),
    path('osimart/quantity-units/', views_osimart.osimart_quantity_units, name='osimart-quantity-units'),
    path('osimart/variant-types/', views_osimart.osimart_variant_types, name='osimart-variant-types'),
    path('osimart/variant-types/<str:vt_id>/', views_osimart.osimart_variant_type_detail, name='osimart-variant-type-detail'),
    path('osimart/announcement-bars/', views_osimart.osimart_announcement_bars, name='osimart-announcement-bars'),
    path('osimart/announcement-bars/<str:ann_id>/', views_osimart.osimart_announcement_bar_detail, name='osimart-announcement-bar-detail'),
    path('osimart/customers/', views_osimart.osimart_customers, name='osimart-customers'),
    path('osimart/medias/', views_osimart.osimart_medias, name='osimart-medias'),
    path('osimart/shipping-zones/', views_osimart.osimart_shipping_zones, name='osimart-shipping-zones'),
    path('osimart/shipping-zones/<str:zone_id>/', views_osimart.osimart_shipping_zone_detail, name='osimart-shipping-zone-detail'),
    path('osimart/order-status-choices/', views_osimart.osimart_order_status_choices, name='osimart-order-status-choices'),
    path('osimart/order-status-choices/<str:status_id>/', views_osimart.osimart_order_status_choice_detail, name='osimart-order-status-choice-detail'),
    path('osimart/cart/view/', views_osimart.osimart_cart_view, name='osimart-cart-view'),
    path('osimart/cart/update-item/', views_osimart.osimart_cart_update_item, name='osimart-cart-update-item'),
]
