from django.contrib import admin
#accessing our models
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(CreditSale)
admin.site.register(Supplier)
admin.site.register(Branch)
