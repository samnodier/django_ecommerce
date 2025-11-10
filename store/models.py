from django.contrib.auth.models import AbstractUser
from django.db import models
from typing import cast


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_vendor = models.BooleanField(default=False)  # type: ignore
    is_customer = models.BooleanField(default=True)  # type: ignore

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_query_name="customuser",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="customuser",
    )

    def __str__(self):
        return self.username


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ("SP", "Shipping"),
        ("BL", "Billing"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    is_default = models.BooleanField(default=False)  # type: ignore

    def __str__(self):
        return f"{self.full_name} ({self.address_type})"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return str(self.name)


class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    sku = models.CharField(max_length=100, unique=True)
    stock_quantity = models.PositiveIntegerField(default=0)  # type: ignore
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart ({cast(User, self.user).username})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # type: ignore

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_number = models.CharField(max_length=20, unique=True)
    shipping_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="shipping_orders"
    )
    billing_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="billing_address"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)  # type: ignore
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{cast(Product, self.product).name} ({self.quantity})"


class Payment(models.Model):
    METHOD_CHOICES = [
        ("card", "Card"),
        ("paypal", "PayPal"),
        ("mobile", "Mobile Money"),
    ]

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment for {cast(Order, self.order).order_number}"


class Shipment(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="shipment"
    )
    carrier = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, default="processing")
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Shipment for Order {cast(Order, self.order).order_number}"


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)  # type: ignore
    comment = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return f"{cast(User, self.user).username}) - {self.product.name}"
