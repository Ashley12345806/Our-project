import django_filters
from .models import Product  # Adjust for your model

class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = [ 'product_name']