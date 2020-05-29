from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, m2m_changed

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.title
class Product(models.Model):
    title = models.CharField(max_length=100)
    isactive = models.BooleanField(default=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='commerce_site/images/')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    amount = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    mail = models.EmailField(max_length=30)
    phone = models.CharField(max_length=15)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

ORDER_STATUS=(
('created','Created'),
('approved','Approved'),
('paid','Paid'),
('delivered','Delivered'),
)

ORDER_PAYMENT=(
('cash','Cash'),
('online','Online'),
)
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS)
    delivery_date = models.DateField(auto_now=False, null=True, blank=True)
    payment = models.CharField(max_length=120, default='cash', choices=ORDER_PAYMENT)
    address = models.TextField()
    total = models.DecimalField(default=0.00, max_digits=100,decimal_places=2)

    def __int__(self):
        return self.customer
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    amount = models.IntegerField()

class Payment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    cvv = models.IntegerField()
    credit = models.DecimalField(max_digits=10,decimal_places=2)

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.customer is None:
                cart_obj.customer = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            print(user)
            print(user.is_authenticated)
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(customer=user_obj)

class Cart(models.Model):
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100,decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100,decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CartManager()

    # def __str__(self):
    #     return self.id
def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        print(action)
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        print(total)
        # if instance.subtotal != instance.total:
        instance.subtotal = total
        print(instance.subtotal)
        instance.save()
m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal + 10
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_receiver, sender=Cart)
