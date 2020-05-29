from django.contrib import admin
from .models import Category
from .models import Product
from .models import UserInfo
from .models import Order
from .models import OrderItem
from .models import Cart
from .models import Payment
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserInfo)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(Payment)
