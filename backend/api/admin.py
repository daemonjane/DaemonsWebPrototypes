from django.contrib import admin
from django.utils.html import format_html, mark_safe

from .models import BackInStockRequest, Category, ContactMessage, Order, OrderItem, Product, Subscription


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "rating", "stock", "image_preview"]
    list_filter = ["category", "rating"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at", "image_preview", "description_preview"]
    fieldsets = [
        (None, {"fields": ["slug", "name", "category"]}),
        ("Pricing & Stock", {"fields": ["price", "stock", "rating"]}),
        ("Description", {"fields": ["description", "description_preview"]}),
        ("Media", {"fields": ["image", "image_preview"]}),
        ("Specifications", {"fields": ["specs"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="field-image_preview" alt="{}" />', obj.image, obj.name
            )
        return mark_safe('<span class="text-slate-600">No image</span>')

    @admin.display(description="Preview")
    def description_preview(self, obj):
        if obj.description:
            return format_html(
                '<div class="field-description_preview">{}</div>',
                obj.description[:300] + "..." if len(obj.description) > 300 else obj.description,
            )
        return mark_safe('<span class="text-slate-600">—</span>')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ["item_total"]
    fields = ["product", "name", "price", "quantity", "item_type", "item_total"]

    @admin.display(description="Total")
    def item_total(self, obj):
        if obj.pk:
            total = obj.price * obj.quantity
            return f"${total:.2f}"
        return "—"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "email", "status", "item_count", "total_value", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "email"]
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]
    readonly_fields = ["created_at", "item_count", "total_value"]
    fieldsets = [
        ("Customer", {"fields": ["name", "email", "address"]}),
        ("Gift Card", {"fields": ["gift_card_code", "gift_card_discount"], "classes": ["collapse"]}),
        ("Fulfillment", {"fields": ["status"]}),
        ("Summary", {"fields": ["item_count", "total_value"]}),
        ("Timestamps", {"fields": ["created_at"], "classes": ["collapse"]}),
    ]

    @admin.display(description="Items")
    def item_count(self, obj):
        return obj.items.count()

    @admin.display(description="Total")
    def total_value(self, obj):
        total = sum(item.price * item.quantity for item in obj.items.all())
        if obj.gift_card_discount:
            total -= obj.gift_card_discount
        return f"${total:.2f}"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["name", "tier", "price", "duration_days", "active", "feature_count"]
    list_filter = ["active", "tier"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "feature_preview"]
    fieldsets = [
        (None, {"fields": ["tier", "name", "price", "duration_days", "active"]}),
        ("Description", {"fields": ["description"]}),
        ("Features", {"fields": ["features", "feature_preview"]}),
        ("Timestamps", {"fields": ["created_at"], "classes": ["collapse"]}),
    ]

    @admin.display(description="Features")
    def feature_count(self, obj):
        return len(obj.features)

    @admin.display(description="Preview")
    def feature_preview(self, obj):
        if obj.features:
            items = "".join(
                f'<li style="color:#94a3b8;font-size:0.75rem;padding:2px 0">{f}</li>'
                for f in obj.features
            )
            return mark_safe(f'<ul style="margin:4px 0;padding-left:16px">{items}</ul>')
        return mark_safe('<span class="text-slate-600">—</span>')


@admin.register(BackInStockRequest)
class BackInStockRequestAdmin(admin.ModelAdmin):
    list_display = ["email", "product_link", "created_at"]
    search_fields = ["email", "product__name"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at"]

    def product_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            f"/admin/api/product/{obj.product.pk}/change/",
            obj.product.name,
        )
    product_link.short_description = "product"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]
    search_fields = ["name", "email", "message"]
    date_hierarchy = "created_at"
    readonly_fields = ["name", "email", "message", "created_at", "message_preview"]
    fieldsets = [
        (None, {"fields": ["name", "email", "message", "message_preview"]}),
        ("Timestamps", {"fields": ["created_at"], "classes": ["collapse"]}),
    ]

    @admin.display(description="Preview")
    def message_preview(self, obj):
        return format_html(
            '<div class="field-description_preview">{}</div>',
            obj.message[:200] + "..." if len(obj.message) > 200 else obj.message,
        )
