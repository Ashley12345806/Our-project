#accessing the django forms module
from django.forms import ModelForm
#accsessing our models to create corresponding forms
from .models import *
from .models import CreditSale,Supplier
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'branch_name', 'product_type', 'time_of_produce', 'stock_contact', 'source', 'cost', 'unit_cost', 'unit_price', 'total_quantity', 'issued_quantity']
        #fields = '__all__'


class SaleForm(ModelForm):
    branch_name = models.CharField(max_length=100, null=True, blank=True)
    customer_name = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.FloatField(default=1, null=True, blank=True)
    unit_price = models.FloatField(default=10, null=True, blank=True)
    amount_received = models.IntegerField(default=10, null=True, blank=True)
    class Meta:
        model = Sale
        fields = ['product', 'branch_name', 'quantity', 'amount_received', 'customer_name', 'salesagent', 'unit_price']
        #fields = '__all__'       


class CreditSaleForm(ModelForm):
    class Meta:
        model = CreditSale
        fields = ['customer_name', 'contact', 'address', 'nin', 'product_name', 'quantity', 'amount_due', 'balance', 'duedate', 'date_of_payment', 'branch_name', 'salesagent']
        #fields = '__all__' 

class AddForm(ModelForm):
    total_quantity = models.FloatField(default=1, null=True, blank=True)
    class Meta:
        model = Product
        fields = ['total_quantity']

class UpdateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['received_quantity'] 


class UserCreation(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2', 
            'address', 
            'phonenumber', 
            'gender', 
            'is_salesagent', 
            'is_manager', 
            'is_owner'
        ]

    def save(self, commit=True):
        user = super(UserCreation, self).save(commit=False)
        if commit:
            user.is_active = True
            user.is_staff = True
            user.save()
        return user


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name', 'contact_number', 'email', 'address', 'branch_name']