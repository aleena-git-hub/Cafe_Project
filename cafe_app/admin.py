from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Category)

admin.site.register(Product)

admin.site.register(Cart)

admin.site.register(CartItem)

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(TableBooking)

admin.site.register(Review)

