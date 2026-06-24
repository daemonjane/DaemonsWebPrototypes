"""Data models for the API app — Products, Cart, Orders, Tracking, Add-ons."""

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """Product category for classifying items."""

    name = models.CharField("name", max_length=100, help_text="Display name for the category")
    slug = models.SlugField("slug", max_length=100, unique=True, help_text="URL-friendly identifier (auto-populated from name)")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Individual product with pricing, specs, and stock tracking."""

    slug = models.SlugField("slug", max_length=100, primary_key=True, help_text="URL-friendly identifier (auto-populated from name)")
    name = models.CharField("name", max_length=200, help_text="The product display name")
    price = models.DecimalField("price", max_digits=8, decimal_places=2, help_text="Current selling price in USD")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name="category",
        help_text="Which category this product belongs to",
    )
    description = models.TextField("description", help_text="Full product description shown on the detail page")
    image = models.CharField("image URL", max_length=500, help_text="URL to the product image (JPG, PNG, or WebP)")
    rating = models.FloatField("rating", help_text="Average customer rating (0.0–5.0)")
    specs = models.JSONField("specifications", default=list, help_text="Key specifications as key-value pairs, e.g. [{'key': 'Weight', 'value': '1.2kg'}]")
    stock = models.IntegerField("stock", null=True, blank=True, help_text="Current inventory count (leave blank for unlimited)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the product was added")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the product was last modified")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Order(models.Model):
    """Customer order with status lifecycle."""

    class Status(models.TextChoices):
        PLACED = "placed", "Order Placed"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        OUT_FOR_DELIVERY = "out_for_delivery", "Out for Delivery"
        DELIVERED = "delivered", "Delivered"

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders",
        verbose_name="user", help_text="The user who placed the order (null for guest)",
    )
    email = models.EmailField("email", help_text="Customer email for order notifications")
    name = models.CharField("name", max_length=200, help_text="Full name for shipping")
    address = models.TextField("address", help_text="Shipping address including street, city, and postal code")
    gift_card_code = models.CharField("gift card code", max_length=50, blank=True, help_text="Optional gift card code to apply discount")
    gift_card_discount = models.DecimalField(
        "gift card discount", max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Discount amount from gift card (auto-calculated)",
    )
    status = models.CharField(
        "status", max_length=20, choices=Status.choices, default=Status.PLACED,
        help_text="Current order status in the fulfillment lifecycle",
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the order was placed")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    """An individual line item within an order."""

    class ItemType(models.TextChoices):
        PRODUCT = "product", "Product"
        UPGRADE = "upgrade", "Upgrade"
        MEMBERSHIP = "membership", "Membership"
        ADDON = "addon", "Add-on"

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="order",
        help_text="The order this item belongs to",
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="product",
        help_text="The product being ordered (optional for custom items)",
    )
    name = models.CharField("name", max_length=200, help_text="Item name shown on the receipt")
    price = models.DecimalField("price", max_digits=8, decimal_places=2, help_text="Unit price at time of purchase")
    quantity = models.PositiveIntegerField("quantity", default=1, help_text="Number of units ordered")
    item_type = models.CharField(
        "item type", max_length=20, choices=ItemType.choices, default=ItemType.PRODUCT,
        help_text="Type of line item: product, upgrade, or membership",
    )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.name} x{self.quantity}"


class Subscription(models.Model):
    """Membership/subscription tier with recurring billing."""

    class Tier(models.TextChoices):
        BASIC = "basic", "Basic"
        PRO = "pro", "Pro"
        ENTERPRISE = "enterprise", "Enterprise"

    tier = models.CharField("tier", max_length=20, choices=Tier.choices, unique=True, help_text="Subscription tier identifier")
    name = models.CharField("name", max_length=100, help_text="Display name for this subscription tier")
    price = models.DecimalField("price", max_digits=8, decimal_places=2, help_text="Monthly price in USD")
    description = models.TextField("description", help_text="Short description of what this tier includes")
    features = models.JSONField("features", default=list, help_text="List of features included in this tier")
    duration_days = models.IntegerField("duration days", default=30, help_text="Billing cycle length in days")
    active = models.BooleanField("active", default=True, help_text="Whether this tier is available for purchase")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the subscription tier was created")

    class Meta:
        ordering = ["price"]
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.name} (${self.price}/mo)"


class BackInStockRequest(models.Model):
    """Notification request for when a product is back in stock."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="back_in_stock_requests", verbose_name="product",
        help_text="The product to be notified about",
    )
    email = models.EmailField("email", help_text="Email address for the notification")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the notification request was created")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Back-in-Stock Request"
        verbose_name_plural = "Back-in-Stock Requests"

    def __str__(self):
        return f"{self.email} - {self.product.name}"


class ContactMessage(models.Model):
    """User-submitted contact form message from the API endpoint."""

    name = models.CharField("name", max_length=200, help_text="Your full name")
    email = models.EmailField("email", help_text="Your email address so we can reply")
    message = models.TextField("message", help_text="How can we help you?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.email}"


class Cart(models.Model):
    """A user's shopping cart (one per user)."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart", verbose_name="user")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the cart was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the cart was last modified")

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    """An individual item within a shopping cart."""

    class ItemType(models.TextChoices):
        PRODUCT = "product", "Product"
        UPGRADE = "upgrade", "Upgrade"
        MEMBERSHIP = "membership", "Membership"
        ADDON = "addon", "Add-on"

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="cart")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="product",
        help_text="The product (null for custom items like upgrades)",
    )
    name = models.CharField("name", max_length=200, help_text="Item display name")
    price = models.DecimalField("price", max_digits=8, decimal_places=2, help_text="Unit price at time of adding")
    quantity = models.PositiveIntegerField("quantity", default=1, help_text="Number of units")
    image = models.CharField("image URL", max_length=500, blank=True, help_text="Image URL (auto-populated for products)")
    item_type = models.CharField(
        "item type", max_length=20, choices=ItemType.choices, default=ItemType.PRODUCT,
        help_text="Product, upgrade, or membership",
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the item was added")

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.name} x{self.quantity}"


class Wishlist(models.Model):
    """A user's wishlist of favorite products."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist", verbose_name="user")
    products = models.ManyToManyField(Product, related_name="wishlists", verbose_name="products")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the wishlist was created")

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return f"Wishlist of {self.user.username}"


class OrderTracking(models.Model):
    """Tracking information for a shipped order."""

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="tracking", verbose_name="order",
        help_text="The order being tracked",
    )
    tracking_number = models.CharField("tracking number", max_length=100, blank=True, help_text="Carrier tracking number")
    carrier = models.CharField("carrier", max_length=100, blank=True, help_text="Shipping carrier name (UPS, FedEx, USPS, etc.)")
    tracking_url = models.URLField("tracking URL", max_length=500, blank=True, help_text="Link to the carrier's tracking page")
    estimated_delivery = models.DateField("estimated delivery", null=True, blank=True, help_text="Estimated delivery date")
    delivered_at = models.DateTimeField("delivered at", null=True, blank=True, help_text="Timestamp when the order was marked delivered")
    notes = models.TextField("notes", blank=True, help_text="Internal shipping notes")

    class Meta:
        verbose_name = "Order Tracking"
        verbose_name_plural = "Order Tracking Records"

    def __str__(self):
        return f"Tracking #{self.tracking_number or 'N/A'} for Order #{self.order_id}"


class ProductAddon(models.Model):
    """Optional add-on / micro-transaction item for a product (e.g. cleaning kit, extended warranty)."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="addons", verbose_name="product",
        help_text="The product this add-on belongs to",
    )
    name = models.CharField("name", max_length=200, help_text="Add-on display name (e.g. 'Cleaning Kit')")
    description = models.TextField("description", blank=True, help_text="Short description of what this add-on includes")
    price = models.DecimalField("price", max_digits=8, decimal_places=2, help_text="Additional cost in USD")
    image = models.CharField("image URL", max_length=500, blank=True, help_text="Optional thumbnail image for the add-on")
    is_available = models.BooleanField("available", default=True, help_text="Whether this add-on can be purchased")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the add-on was created")

    class Meta:
        ordering = ["name"]
        verbose_name = "Product Add-on"
        verbose_name_plural = "Product Add-ons"

    def __str__(self):
        return f"{self.name} (+${self.price}) for {self.product.name}"


class TrackingHistory(models.Model):
    """A single status event in the order tracking timeline."""

    tracking = models.ForeignKey(
        OrderTracking, on_delete=models.CASCADE, related_name="history", verbose_name="tracking",
        help_text="The tracking record this event belongs to",
    )
    status = models.CharField("status", max_length=100, help_text="Status label (e.g. 'Picked Up', 'In Transit', 'Out for Delivery')")
    location = models.CharField("location", max_length=200, blank=True, help_text="City/state where the event occurred")
    note = models.TextField("note", blank=True, help_text="Details about this tracking event")
    timestamp = models.DateTimeField("timestamp", help_text="When this event occurred")

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Tracking History Entry"
        verbose_name_plural = "Tracking History Entries"

    def __str__(self):
        return f"{self.status} at {self.timestamp}"

@property
def status_label(self):
    return Order.Status(self.status).label if self.status else ""
Order.status_label = status_label
del status_label
