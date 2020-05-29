from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from .models import Category, Product, UserInfo, Order, OrderItem, Cart, Payment
from .forms import CustInfo, OrderHeader, OnlinePayment
from django.views.generic import DetailView, ListView

# Create your views here.
def home(request):
    categories = Category.objects.filter(isactive = True)
    products = Product.objects.filter(isactive = True).order_by('-id')[:3]
    products_cat = list()
    for cat in categories:
        products_cat.extend(Product.objects.filter(category=cat.id, isactive = True).order_by('-id')[:3])
    return render(request, 'commerce_site\home.html', {'categories':categories, 'products':products, 'products_cat':products_cat})

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'commerce_site\signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'commerce_site\signupuser.html',{'form':UserCreationForm(),'error':'Username has already been taken please choose another name'})
        else:
            return render(request, 'commerce_site\signupuser.html',{'form':UserCreationForm(),'error':'Passwords didnot match'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        pass

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'commerce_site\loginuser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'commerce_site\loginuser.html',{'form':AuthenticationForm(), 'error':'Wrong Credintials'})
        else:
            login(request, user)
            return redirect('home')

def content(request, cat_pk):
    category = get_object_or_404(Category,pk =cat_pk)
    products = Product.objects.filter(category=cat_pk)
    return render(request, 'commerce_site\content.html',{'products':products,'category':category})


def product(request, prod_pk):
    product = get_object_or_404(Product,pk = prod_pk)
    return render(request, 'commerce_site\product.html',{'product':product})

def newsignup(request):
    return render(request, 'commerce_site\signup2.html',{'form':UserCreationForm()})

def search(request):
    query = request.GET.get('q')
    if query is not None:
        lookups = Q(title__icontains=query) | Q(description__icontains=query)
        products = Product.objects.filter(lookups).distinct()
    else:
        products = Product.objects.none()
    return render(request, 'commerce_site\content.html',{'products':products})

def custinfo(request):
    filteredinfo = UserInfo.objects.filter(customer=request.user).count()
    # userinfo = None
    if request.method == 'GET':
        if filteredinfo > 0:
            userinfo=get_object_or_404(UserInfo,customer =request.user)
            form = CustInfo(instance=userinfo)
            return render(request, 'commerce_site\custinfo.html',{'form':form, 'userinfo':userinfo, 'filteredinfo':filteredinfo})
        else:
            return render(request, 'commerce_site\custinfo.html',{'form':CustInfo(),'filteredinfo':filteredinfo})
    else:
        if filteredinfo == 0:
            try:
                form = CustInfo(request.POST)
                newinfo = form.save(commit=False)
                newinfo.customer = request.user
                newinfo.save()
                # return HttpResponseRedirect(request.path_info)
                return render(request, 'commerce_site\success.html', {'title':'Well Done', 'body':'Profile saved successfully'})
            except ValueError:
                return render(request, 'commerce_site\custinfo.html',{'form':CustInfo(), 'error':'Something wrong with your data', 'success':'Your profile data saved'})
        else:
            userinfo=get_object_or_404(UserInfo,customer =request.user)
            try:
                upform = CustInfo(request.POST, instance=userinfo)
                upform.save()
                # return HttpResponseRedirect(request.path_info)
                return render(request, 'commerce_site\success.html', {'title':'Well Done', 'body':'Profile updated successfully'})
            except ValueError:
                return render(request, 'commerce_site\custinfo.html',{'form':CustInfo(), 'error':'Something wrong with your data', 'success':'Your profile data updated'})
def success(request):
    return render(request, 'commerce_site\success.html', {'title':'Well Done', 'body':'Profile updated successfully'})

def orders(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'commerce_site\orders.html', {'orders':orders})

def details(request, order_pk):
    order = get_object_or_404(Order,pk=order_pk )
    details = OrderItem.objects.filter(order=order_pk)
    return render(request, 'commerce_site\details.html', {'order':order, 'details':details})

def cart(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # products = cart_obj.products.all()
    # total = 0
    # for x in products:
    #     total += x.price
    # print(total)
    # cart_obj.total = total
    # cart_obj.save()
    return render(request, 'commerce_site\cart.html',{'cart':cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    product_obj = Product.objects.get(id = product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)
    request.session['cart_items'] = cart_obj.products.count()
    return redirect('cart')
    # return HttpResponseRedirect(request.path_info)
    # return redirect(product_obj.get_absolute_url())

def checkout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'commerce_site\checkout.html',{'form':OrderHeader()})
        else:
            return redirect('loginuser')
    else:
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        order = Order.objects.create(customer=request.user, address=request.POST['address'], payment='cash', total=cart_obj.total)
        order.save()
        # print(cart_obj)
        order_items = []
        prods = []
        batch_size = cart_obj.products.all().count()
        price = 0
        amount = 0
        order_amount = 0
        if order.id > 0:
            for product in cart_obj.products.all():
                # order_amount = product.amount
                prod = get_object_or_404(Product,pk =product.id)
                price = prod.price
                amount = prod.amount - 1
                order_items.append(OrderItem(order_id=order.id, product_id=product.id, price=price,amount=1))
                prods.append(Product(id =product.id, amount = amount))
                # print(order_items)
            items = OrderItem.objects.bulk_create(order_items,batch_size)
            Product.objects.bulk_update(prods,['amount'])
            cart_obj.delete()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return render(request, 'commerce_site\success.html', {'title':'Congratulations', 'body':'Order saved successfully'})
        else:
            return render(request, 'commerce_site\checkout.html',{'form':OrderHeader(),'error':'Error order didn\'t saved'})

def payment(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'commerce_site\payment.html',{'form':OrderHeader()})
        else:
            return redirect('loginuser')
    else:
        payment = get_object_or_404(Payment,customer =request.user)
        print(payment)
        print(request.POST['expiry_year'])
        print(payment.year)
        print(int(request.POST['expiry_year']) == int(payment.year))
        if request.POST['holdername'] != payment.name or request.POST['holdername'] is None:
            return render(request, 'commerce_site\payment.html',{'form':OrderHeader(),'error':'Incorrect card holder name'})
        if int(request.POST['cardnumber']) != int(payment.number) or int(request.POST['cardnumber']) is None or len(request.POST['cardnumber']) != 14:
            return render(request, 'commerce_site\payment.html',{'form':OrderHeader(),'error':'Incorrect card number'})
        if int(request.POST['expiry_month']) != int(payment.month):
            return render(request, 'commerce_site\payment.html',{'form':OrderHeader(),'error':'Incorrect month'})
        if int(request.POST['expiry_year']) != int(payment.year):
            return render(request, 'commerce_site\payment.html',{'form':OrderHeader(),'error':'Incorrect year'})
        if int(request.POST['cvv']) != int(payment.cvv):
            return render(request, 'commerce_site\payment.html',{'form':OrderHeader(),'error':'Incorrect cvv'})
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if float(cart_obj.total) > float(payment.credit):
            return render(request, 'commerce_site\payment.html',{'form':OrderHeader(),'error':'Not enough credit'})
        order = Order.objects.create(customer=request.user, address=request.POST['address'], payment='online', total=cart_obj.total, status='paid')
        order.save()
        # print(cart_obj)
        order_items = []
        prods = []
        batch_size = cart_obj.products.all().count()
        price = 0
        amount = 0
        order_amount = 0
        if order.id > 0:
            for product in cart_obj.products.all():
                # order_amount = product.amount
                prod = get_object_or_404(Product,pk =product.id)
                price = prod.price
                amount = prod.amount - 1
                order_items.append(OrderItem(order_id=order.id, product_id=product.id, price=price,amount=1))
                prods.append(Product(id =product.id, amount = amount))
                # print(order_items)
            items = OrderItem.objects.bulk_create(order_items,batch_size)
            Product.objects.bulk_update(prods,['amount'])
            cart_obj.delete()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return render(request, 'commerce_site\success.html', {'title':'Congratulations', 'body':'Order saved successfully'})
        else:
            return render(request, 'commerce_site\payment.html',{'form':OrderHeader(),'error':'Error order didn\'t saved'})

class ProductDetail(DetailView):
    model = Product
    template_name = 'commerce_site/product.html'
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(ProductDetail, self).get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
