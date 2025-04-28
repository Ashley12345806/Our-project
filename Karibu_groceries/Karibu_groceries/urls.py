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
#accessing our views from  kgl_app
from kgl_app import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('home/', views.index, name='home'),
    path('sales/', views.sales, name='sales'),
    path('', auth_views.LoginView.as_view(template_name='kgl_app/login.html'), name='login'),
    path('login/',views.Login,name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('managerdashboard/', views.managerdashboard, name='managerdashboard'),
    path('logout/', views.logout, name='logout'),
    path('products/', views.products, name='products'),
    path('productdetail/<int:product_id>/', views.product_detail, name='productdetail'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('issue_item/<str:pk>/', views.issue_item, name='issue_item'),
    path('receipt/', views.receipt, name='receipt'),
    path('receipt/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
    path('add_to_stock/<str:pk>/', views.add_to_stock, name='add_to_stock'),
    path('addproduct/<int:pk>/', views.addproduct, name='addproduct'), 
    path('deferredpaymentlist/',views.deferredpaymentlist, name ='deferredpaymentlist'),
    path('deferredpayment/', views.deferredpayment, name='deferredpayment'),
    path('signup/', views.signup, name='signup'),
    
  
]
