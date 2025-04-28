# kgl_app/models.py

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


class UserProfile(AbstractUser):
    is_salesagent = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    address = models.CharField(blank=True, max_length=50)
    phonenumber = models.CharField(blank=True, max_length=20)
    gender = models.CharField(
        blank=True,
        max_length=20,
        choices=[('Female', 'Female'), ('Male', 'Male')]
    )

    def __str__(self):
        return self.username


class Product(models.Model):
    
    product_name=models.CharField(max_length=50, blank=False, default='')
    branch_name=models.CharField(max_length=50,  blank=True, null=True)
    product_type=models.CharField(max_length=50, null = True, blank=True)
    time_of_produce=models.CharField(max_length=50, null = True, blank=True)
    stock_contact=models.CharField(max_length=50, null = True, blank=True)
    source = models.CharField(max_length=50, default='',blank=False)
    cost = models.FloatField(default=0, null = False, blank=False)
    unit_cost = models.FloatField(default=10, null = False, blank=False)
    unit_price = models.FloatField(default=0, null = False, blank=False)
    total_quantity = models.FloatField(default=0, null = False, blank=False)
    received_quantity = models.FloatField(default=0, null = False, blank=False)
    issued_quantity = models.FloatField(default=0, null = False, blank=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    



class Sale(models.Model):
    product = models.CharField(max_length=50,  blank=False, default='')
    branch_name = models.CharField(max_length=100, blank=False, null=False, default='')
    quantity = models.FloatField(default=10, null=False, blank=False)
    amount_received = models.IntegerField(default=10, null=False, blank=False)
    customer_name = models.CharField(max_length=50, null=False, blank=False, default='')
    salesagent = models.CharField(max_length=50, null=False, blank=False, default='')
    unit_price = models.FloatField(default=10, null=False, blank=False)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)


    #getting the total amount of the sale
    def get_total(self):
        total = self.quantity * self.unit_price
        return int(total)
    
    #getting change
    def get_change(self):
        change = self.get_total() - self.amount_received
        return abs(int(change))
    
    def __str__(self):
        return self.product
    

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
    
    def clean(self):
        #check if nin is valid
        if not self.nin:
            raise ValidationError("NIN is required.")
        




    

    

