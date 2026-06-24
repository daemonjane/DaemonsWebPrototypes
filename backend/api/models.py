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
    created_at = models.DateTimeField(auto_now_add=True)

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
