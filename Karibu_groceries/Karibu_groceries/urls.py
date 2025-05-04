"""
URL configuration for Karibu_groceries project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from kgl_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('home/', views.index, name='home'),
    path('sales/', views.sales, name='sales'),
    path('login/', views.Login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('managerdashboard/', views.managerdashboard, name='managerdashboard'),
    path('logout/', views.logout, name='logout'),
    path('products/', views.products, name='products'),
    path('productdetail/<int:product_id>/', views.product_detail, name='productdetail'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('issue_item/<int:pk>/', views.issue_item, name='issue_item'),
    path('receipt/', views.receipt, name='receipt'),
    path('receipt/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
    path('add_to_stock/<int:pk>/', views.add_to_stock, name='add_to_stock'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('addproduct/<int:pk>/', views.addproduct, name='addproduct_with_pk'),
    path('creditsaleslist/', views.creditsaleslist, name='creditsaleslist'),
    path('creditsales/', views.creditsales, name='creditsales'),
    path('supplier/', views.supplier_list, name='supplier'),
    path('supplier/<int:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    path('supplier/add/', views.add_supplier, name='add_supplier'),
    path('supplier/<int:supplier_id>/edit/', views.edit_supplier, name='edit_supplier'),
    path('supplier/<int:supplier_id>/delete/', views.delete_supplier, name='delete_supplier'),
    path('signup/', views.signup, name='signup'),
]
