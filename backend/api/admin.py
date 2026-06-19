from django.contrib import admin

from .models import BackInStockRequest, Category, ContactMessage, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "rating", "stock"]
    list_filter = ["category", "rating"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created_at"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "email", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "email"]
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]


@admin.register(BackInStockRequest)
class BackInStockRequestAdmin(admin.ModelAdmin):
    list_display = ["email", "product", "created_at"]
    search_fields = ["email", "product__name"]
    date_hierarchy = "created_at"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]
    search_fields = ["name", "email", "message"]
    date_hierarchy = "created_at"
    readonly_fields = ["name", "email", "message", "created_at"]
