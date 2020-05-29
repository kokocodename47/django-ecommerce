from django import forms
from django.forms import ModelForm
from .models import UserInfo, Order, Payment
class CustInfo(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['full_name', 'address', 'mail', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control'}),
            'mail': forms.EmailInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'})
        }
class OrderHeader(ModelForm):
    class Meta:
        model = Order
        fields = ['address']
        widgets = {
            'address': forms.Textarea(attrs={'class':'form-control'})
            # 'payment': forms.Select(attrs={'class':'form-control'})
        }

class OnlinePayment(ModelForm):
    class Meta:
        model = Payment
        fields = ['name','number','year','month','cvv']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'number':forms.IntegerField(),
            'year':forms.IntegerField(),
            'month':forms.IntegerField(),
            'cvv':forms.IntegerField()
            # 'payment': forms.Select(attrs={'class':'form-control'})IntegerField
        }
