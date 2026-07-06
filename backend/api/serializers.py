"""DRF serializers for API models — Cart, Orders, Products, Add-ons."""

from rest_framework import serializers

from .models import Cart, CartItem, Order, OrderItem, OrderTracking, ProductAddon, TrackingHistory, Wishlist


class CartItemSerializer(serializers.ModelSerializer):
    product_slug = serializers.SlugField(source="product.slug", read_only=True, allow_null=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product_slug", "product_image", "name", "price", "quantity", "image", "item_type", "created_at"]

    def get_product_image(self, obj):
        if obj.image:
            return obj.image
        if obj.product and obj.product.image:
            return obj.product.image
        return ""


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price", "total_items", "created_at", "updated_at"]

    def get_total_price(self, obj):
        return round(sum(float(item.price) * item.quantity for item in obj.items.all()), 2)

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())


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
        fields = ["id", "email", "name", "address", "status", "items", "total", "gift_card_code", "gift_card_discount", "has_tracking", "created_at"]

    def get_total(self, obj):
        total = sum(float(item.price) * item.quantity for item in obj.items.all())
        if obj.gift_card_discount:
            total -= float(obj.gift_card_discount)
        return round(total, 2)

    def get_has_tracking(self, obj):
        return hasattr(obj, "tracking") and bool(obj.tracking.tracking_number)
