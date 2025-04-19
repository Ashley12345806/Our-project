from django.db import models
from datetime import datetime

# Create your models here.
class Product(models.Model):
    
    product_name=models.CharField(max_length=50, null = True, blank=True)
    branch_name=models.CharField(max_length=50, null = True, blank=True)
    product_type=models.CharField(max_length=50, null = True, blank=True)
    time_of_produce=models.CharField(max_length=50, null = True, blank=True)
    stock_contact=models.CharField(max_length=50, null = True, blank=True)
    source = models.CharField(max_length=50, null = True, blank=True)
    cost = models.FloatField(default=0, null = True, blank=True)
    unit_cost = models.FloatField(default=10, null = True, blank=True)
    unit_price = models.FloatField(default=0, null = True, blank=True)
    quantity = models.FloatField(default=0, null = True, blank=True)
    issued_quantity = models.FloatField(default=0, null = True, blank=True)
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return self.product_name
    



class Sale(models.Model):
    product_name = models.CharField(max_length=50, null=True, blank=True)
    branch_name = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.FloatField(default=10, null=True, blank=True)
    amount_received = models.IntegerField(default=10, null=True, blank=True)
    issued_to = models.CharField(max_length=50, null=True, blank=True)
    salesagent = models.CharField(max_length=50, null=True, blank=True)
    unit_price = models.FloatField(default=10, null=True, blank=True)
    date = models.DateField(default=datetime.now)
    time = models.TimeField(default=datetime.now)



class Deffered_payment(models.Model):
    customer_name = models.CharField(max_length=25, null=True, blank=True)
    contact = models.CharField( max_length=50,null=True, blank=True)
    address = models.CharField(max_length=20, null=True, blank=True)
    nin = models.CharField(max_length=50, null=True, blank=True, unique=True)
    product_name = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.FloatField(default=0, null=True, blank=True)
    amount_due = models.FloatField(default=0, null=True, blank=True)
    balance = models.FloatField(default=0, null=True, blank=True)
    duedate = models.DateField(default=datetime.now)
    date_of_payment = models.DateField(default=datetime.now)
    branch_name = models.CharField(max_length=50, null=True, blank=True)
    salesagent = models.CharField(max_length=50, null=True, blank=True)
    date_of_dispatch = models.DateField(default=datetime.now)

    def __str__(self):
        return self.customer_name




    

    

