#accessing the django forms module
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'branch', 'product_type', 'time_of_produce', 'stock_contact', 'source', 'cost', 'unit_cost', 'unit_price', 'total_quantity', 'issued_quantity']


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'branch', 'quantity', 'amount_received', 'customer_name', 'salesagent', 'unit_price']

    def __init__(self, user, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        if user.is_salesagent and user.branch:
            self.fields['branch'].initial = user.branch
            self.fields['branch'].disabled = True
            self.fields['salesagent'].initial = user.username
            self.fields['salesagent'].disabled = True


class CreditSaleForm(ModelForm):
    class Meta:
        model = CreditSale
        fields = ['customer_name', 'contact', 'address', 'nin', 'product_name', 'quantity', 'amount_due', 'balance', 'duedate', 'date_of_payment', 'branch', 'salesagent']

    def __init__(self, user, *args, **kwargs):
        super(CreditSaleForm, self).__init__(*args, **kwargs)
        if user.is_salesagent and user.branch:
            self.fields['branch'].initial = user.branch
            self.fields['branch'].disabled = True
            self.fields['salesagent'].initial = user.username
            self.fields['salesagent'].disabled = True


class AddForm(ModelForm):
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
            'is_owner',
            'branch'
        ]

    def clean(self):
        cleaned_data = super().clean()
        is_salesagent = cleaned_data.get('is_salesagent')
        is_manager = cleaned_data.get('is_manager')
        branch = cleaned_data.get('branch')
        if (is_salesagent or is_manager) and not branch:
            raise forms.ValidationError("A branch must be selected for sales agents and managers.")
        return cleaned_data

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
        fields = ['supplier_name', 'contact_number', 'email', 'address', 'branch']

