"""DRF serializers for API models — Cart, Orders, Products, Add-ons."""

from rest_framework import serializers

from .models import BackInStockRequest, Order, OrderItem, OrderTracking, ProductAddon, TrackingHistory, Wishlist


class ProductAddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAddon
        fields = ["id", "name", "description", "price", "image", "is_available"]


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ["id", "product_slugs", "created_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    product_slug = serializers.SlugField(source="product.slug", read_only=True, allow_null=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product_slug", "name", "price", "quantity", "item_type"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    has_tracking = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "email", "name", "address", "status", "items", "total", "gift_card_code", "gift_card_discount", "has_tracking", "payment_intent_id", "payment_status", "created_at"]

    def get_total(self, obj):
        total = sum(float(item.price) * item.quantity for item in obj.items.all())
        if obj.gift_card_discount:
            total -= float(obj.gift_card_discount)
        return round(total, 2)

    def get_has_tracking(self, obj):
        return hasattr(obj, "tracking") and bool(obj.tracking.tracking_number)


class BackInStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackInStockRequest
        fields = ["product_slug", "product_name", "email"]
