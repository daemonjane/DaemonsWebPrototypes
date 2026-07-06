"""Admin configuration for api app — Products, Orders, Tracking, Add-ons."""

from django.contrib import admin
from django.utils.html import format_html, mark_safe

from .models import BackInStockRequest, Cart, CartItem, Category, ContactMessage, Order, OrderItem, OrderTracking, Product, ProductAddon, Subscription, TrackingHistory, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 25


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
    list_display = ["pk", "user", "name", "email", "status", "item_count", "total_value", "track_order", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "email", "address"]
    date_hierarchy = "created_at"
    list_per_page = 25
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

    @admin.display(description="Tracking")
    def track_order(self, obj):
        if hasattr(obj, "tracking") and obj.tracking.tracking_number:
            url = obj.tracking.tracking_url or "#"
            return format_html(
                '<a href="{}" target="_blank" style="color:#06b6d4;font-weight:600;">📦 Track #{}</a>',
                url, obj.tracking.tracking_number,
            )
        return format_html(
            '<a href="/admin/api/ordertracking/add/?order={}" style="color:#94a3b8;">➕ Add Tracking</a>',
            obj.pk,
        )


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
    list_display = ["email", "product", "created_at"]
    search_fields = ["email", "product__name"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at"]
    list_per_page = 25


@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ["order", "carrier", "tracking_number", "estimated_delivery", "delivered_at"]
    search_fields = ["tracking_number", "carrier", "order__name", "order__email"]
    list_filter = ["carrier"]
    date_hierarchy = "estimated_delivery"
    fieldsets = [
        ("Order", {"fields": ["order"]}),
        ("Tracking Info", {"fields": ["tracking_number", "carrier", "tracking_url"]}),
        ("Dates", {"fields": ["estimated_delivery", "delivered_at"]}),
        ("Notes", {"fields": ["notes"], "classes": ["collapse"]}),
    ]

    @admin.display(description="Order")
    def order_link(self, obj):
        return format_html('<a href="/admin/api/order/{}/change/">Order #{}</a>', obj.order_id, obj.order_id)


@admin.register(TrackingHistory)
class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = ["tracking", "status", "location", "timestamp"]
    list_filter = ["status"]
    search_fields = ["status", "location", "tracking__tracking_number"]
    date_hierarchy = "timestamp"


@admin.register(ProductAddon)
class ProductAddonAdmin(admin.ModelAdmin):
    list_display = ["name", "product_slug", "price", "is_available", "created_at"]
    list_filter = ["is_available"]
    search_fields = ["name", "description", "product_slug"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]
    search_fields = ["name", "email", "message"]
    date_hierarchy = "created_at"
    list_per_page = 25
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


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ["created_at"]
    fields = ["product", "name", "price", "quantity", "item_type", "created_at"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["name", "cart", "price", "quantity", "item_type", "created_at"]
    search_fields = ["name", "cart__user__username"]
    list_filter = ["item_type"]
    date_hierarchy = "created_at"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "item_count", "total", "created_at", "updated_at"]
    search_fields = ["user__username", "user__email"]
    date_hierarchy = "created_at"
    inlines = [CartItemInline]
    readonly_fields = ["created_at", "updated_at"]

    @admin.display(description="Items")
    def item_count(self, obj):
        return obj.items.count()

    @admin.display(description="Total")
    def total(self, obj):
        total = sum(float(item.price) * item.quantity for item in obj.items.all())
        return f"${total:.2f}"


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "product_count", "created_at"]
    search_fields = ["user__username", "user__email"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "product_slugs"]

    @admin.display(description="Products")
    def product_count(self, obj):
        return len(obj.product_slugs)
