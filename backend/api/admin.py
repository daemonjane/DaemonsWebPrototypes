from django.contrib import admin

from .models import BackInStockRequest, Category, ContactMessage, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "rating", "stock"]
    list_filter = ["category"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "email", "status", "created_at"]
    list_filter = ["status"]
    inlines = [OrderItemInline]


@admin.register(BackInStockRequest)
class BackInStockRequestAdmin(admin.ModelAdmin):
    list_display = ["email", "product", "created_at"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]
