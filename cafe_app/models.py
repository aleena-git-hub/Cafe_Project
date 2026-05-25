from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# CATEGORY
   

class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



# PRODUCT / MENU ITEMS
   

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    photo = models.ImageField(upload_to='products/')

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# CART
   


class Cart(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# CART ITEMS
   

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

    @property
    def total_price(self):
        return self.quantity * self.product.price



# ORDER
   

class Order(models.Model):

    STATUS_CHOICES = (

    ('Pending', 'Pending'),
    ('Preparing', 'Preparing'),
    ('Packing', 'Packing'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),

    )
    PAYMENT_CHOICES = (

        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Card', 'Card'),

    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    customer_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"



# ORDER ITEMS
   

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.product.name



# TABLE BOOKING
   


# =========================
# CAFE TABLE
# =========================

class CafeTable(models.Model):

    table_number = models.PositiveIntegerField(unique=True)

    seats = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number} - {self.seats} Seats"


# =========================
# TABLE BOOKING
# =========================

class TableBooking(models.Model):

    STATUS_CHOICES = (

        ('Reserved', 'Reserved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_bookings', null=True, blank=True)

    customer_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    guests = models.PositiveIntegerField()

    booking_date = models.DateField()

    booking_time = models.TimeField()

    end_time = models.TimeField()

    tables = models.ManyToManyField(CafeTable)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Reserved'
    )

    special_request = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

 
# REVIEW
   

class Review(models.Model):

    customer_name = models.CharField(max_length=100)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name
    
class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    def __str__(self):

        return self.user.username
    
