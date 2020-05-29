"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from commerce_site import views, models
from django.conf.urls.static import static
# from django.conf.urls import handler404, handler500
from django.conf import settings
from commerce_site.models import Product
from commerce_site.views import  ProductDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # Auth
    path('signup/',views.signupuser,name='signupuser'),
    path('logout/',views.logoutuser,name='logoutuser'),
    path('login/',views.loginuser,name='loginuser'),
    path('custinfo/',views.custinfo,name='custinfo'),

    # site
    path('content/<int:cat_pk>',views.content,name='content'),
    url(r'product/(?P<pk>\d+)/$',ProductDetail.as_view(),name='product'),
    path('search/',views.search,name='search'),
    path('success/',views.success,name='success'),
    path('orders/',views.orders,name='orders'),
    path('details/<int:order_pk>',views.details,name='details'),
    path('cart/',views.cart,name='cart'),
    path('cart_update/',views.cart_update,name='cart_update'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    # test
    path('newsignup/',views.newsignup,name='newsignup'),

]

urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

admin.site.site_header = "Onlineshop Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to our onlineshop"
# handler404 = views.notfound
