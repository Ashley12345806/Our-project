# kgl_app/models.py

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


class Branch(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False,default='')

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    is_salesagent = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    address = models.CharField(max_length=50, blank=False)
    phonenumber = models.CharField(max_length=20, blank=False)
    gender = models.CharField(
        max_length=20,
        choices=[('Female', 'Female'), ('Male', 'Male')],
        blank=True
    )
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL,null=True, blank=False)

    def __str__(self):
        return self.username

    def clean(self):
        if (self.is_manager or self.is_salesagent) and not self.branch:
            raise ValidationError("Managers and sales agents must be assigned to a branch.")


class Product(models.Model):
    product_name = models.CharField(max_length=50, blank=False, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=False,default='')
    product_type = models.CharField(max_length=50, blank=True)
    time_of_produce = models.CharField(max_length=50, blank=True)
    stock_contact = models.CharField(max_length=50, blank=True)
    source = models.CharField(max_length=50)
    cost = models.FloatField(default=2)
    unit_cost = models.FloatField(default=2)
    unit_price = models.FloatField(default=2)
    total_quantity = models.FloatField(default=2)
    received_quantity = models.FloatField(default=2)
    issued_quantity = models.FloatField(default=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product_name


class Sale(models.Model):
    product = models.CharField(max_length=50, blank=False, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=False,null= True,default='')
    quantity = models.FloatField(default=0)
    amount_received = models.IntegerField(default=0)
    customer_name = models.CharField(max_length=50)
    salesagent = models.CharField(max_length=50)
    unit_price = models.FloatField(default=2)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def get_total(self):
        total = self.quantity * self.unit_price
        return int(total)

    def get_change(self):
        change = self.get_total() - self.amount_received
        return abs(int(change))

    def __str__(self):
        return self.product


class CreditSale(models.Model):
    customer_name = models.CharField(max_length=25, blank=False, null=False)
    contact = models.CharField(max_length=50, blank=False, null=False)
    address = models.CharField(max_length=20, blank=False, null=False)
    nin = models.CharField(max_length=50, blank=False, null=False, unique=True)
    product_name = models.CharField(max_length=50, blank=False, null=False)
    quantity = models.FloatField(default=2, blank=False, null=False)
    amount_due = models.FloatField(default=2, blank=False, null=False)
    balance = models.FloatField(default=2, blank=False, null=False)
    duedate = models.DateField(default=timezone.now)
    date_of_payment = models.DateField(default=timezone.now)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=False, null=True,default='')
    salesagent = models.CharField(max_length=50, blank=False, null=False)
    date_of_dispatch = models.DateField(default=timezone.now)

    def __str__(self):
        return self.customer_name or "Unnamed Credit Sale"

    def clean(self):
        if not self.nin:
            raise ValidationError("NIN is required.")


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100, blank=False, null=False)
    contact_number = models.CharField(max_length=20, blank=False, null=False)
    email = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=False, null=False,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['supplier_name']
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

    def __str__(self):
        return self.supplier_name