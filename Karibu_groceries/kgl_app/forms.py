#accessing the django forms module
from django.forms import ModelForm
#accsessing our models to create corresponding forms
from .models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'branch_name', 'product_type', 'time_of_produce', 'stock_contact', 'source', 'cost', 'unit_cost', 'unit_price', 'quantity', 'issued_quantity', 'date']
        #fields = '__all__'


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['product_name', 'branch_name', 'quantity', 'amount_received', 'issued_to', 'salesagent', 'unit_price', 'date', 'time']
        #fields = '__all__'       
