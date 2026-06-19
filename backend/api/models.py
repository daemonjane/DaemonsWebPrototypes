from django.db import models


class Category(models.Model):
    """Product category for classifying items."""

    name = models.CharField("name", max_length=100)
    slug = models.SlugField("slug", max_length=100, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Individual product with pricing, specs, and stock tracking."""

    slug = models.SlugField("slug", max_length=100, primary_key=True)
    name = models.CharField("name", max_length=200)
    price = models.DecimalField("price", max_digits=8, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name="category"
    )
    description = models.TextField("description")
    image = models.CharField("image URL", max_length=500)
    rating = models.FloatField("rating")
    specs = models.JSONField("specifications", default=list)
    stock = models.IntegerField("stock", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    email = models.EmailField("email")
    name = models.CharField("name", max_length=200)
    address = models.TextField("address")
    gift_card_code = models.CharField("gift card code", max_length=50, blank=True)
    gift_card_discount = models.DecimalField(
        "gift card discount", max_digits=5, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(
        "status", max_length=20, choices=Status.choices, default=Status.PLACED
    )
    created_at = models.DateTimeField(auto_now_add=True)

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
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="order"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="product"
    )
    name = models.CharField("name", max_length=200)
    price = models.DecimalField("price", max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField("quantity", default=1)
    item_type = models.CharField(
        "item type", max_length=20, choices=ItemType.choices, default=ItemType.PRODUCT
    )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.name} x{self.quantity}"


class BackInStockRequest(models.Model):
    """Notification request for when a product is back in stock."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="back_in_stock_requests", verbose_name="product"
    )
    email = models.EmailField("email")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Back-in-Stock Request"
        verbose_name_plural = "Back-in-Stock Requests"

    def __str__(self):
        return f"{self.email} - {self.product.name}"


class ContactMessage(models.Model):
    """User-submitted contact form message from the API endpoint."""

    name = models.CharField("name", max_length=200)
    email = models.EmailField("email")
    message = models.TextField("message")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.email}"
