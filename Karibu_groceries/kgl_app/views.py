from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from .filters import ProductFilter
from kgl_app.models import *
from kgl_app.forms import *
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, "kgl_app/index.html")

def index(request):
    products = Product.objects.all().order_by('id')
    return render(request, "kgl_app/home.html", {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'kgl_app/productdetail.html', {'product': product})

@login_required
def delete_product(request, product_id):
    if not request.user.is_manager:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    product = Product.objects.get(id=product_id)
    product.delete()
    return HttpResponseRedirect(reverse('products'))

@login_required
def edit_product(request, product_id):
    if not request.user.is_manager:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'kgl_app/edit_product.html', {'form': form, 'product': product})

@login_required
def issue_item(request, pk):
    if not request.user.is_salesagent:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    issued_product = Product.objects.get(id=pk)
    sales_form = SaleForm(request.POST or None)
    if request.method == 'POST':
        if sales_form.is_valid():
            new_sale = sales_form.save(commit=False)
            new_sale.product = issued_product.product_name
            new_sale.unit_price = issued_product.unit_price
            new_sale.save()
            issued_quantity = int(request.POST['quantity'])
            issued_product.total_quantity -= issued_quantity
            issued_product.save()
            return redirect('receipt')
    return render(request, "kgl_app/issue_item.html", {'sales_form': sales_form})

@login_required
def sales(request):
    if not request.user.is_owner:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    sales = Sale.objects.all().order_by('id')
    total_expected = sum([products.get_total() or 0 for products in sales])
    total = sum([products.amount_received or 0 for products in sales])
    total_change = sum([products.get_change() or 0 for products in sales])
    net = total_expected - total
    return render(request, "kgl_app/sales.html", {
        'sales': sales,
        'total_expected': total_expected,
        'total': total,
        'total_change': total_change,
        'net': net
    })

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_owner == True:
            form = login(request, user)
            return redirect('/dashboard')
        if user is not None and user.is_salesagent == True:
            form = login(request, user)
            return redirect('/products')
        if user is not None and user.is_manager == True:
            form = login(request, user)
            return redirect('/managerdashboard')
        else:
            print('Something went wrong')
    form = AuthenticationForm()
    return render(request, 'kgl_app/login.html', {'form': form, 'title': 'Login'})

@login_required
def dashboard(request):
    if not request.user.is_owner:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    total_sales = Sale.objects.aggregate(total=Sum('amount_received'))['total'] or 0
    total_receipts = Sale.objects.count()
    total_products = Product.objects.count()
    total_branches = Product.objects.values('branch_name').distinct().count()
    context = {
        'user': request.user,
        'total_sales': total_sales,
        'total_receipts': total_receipts,
        'total_products': total_products,
        'total_branches': total_branches,
    }
    return render(request, 'kgl_app/dashboard.html', context)

@login_required
def managerdashboard(request):
    if not request.user.is_manager:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    total_sales = Sale.objects.aggregate(total=Sum('amount_received'))['total'] or 0
    total_receipts = Sale.objects.count()
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    pending_credits = CreditSale.objects.count()
    context = {
        'user': request.user,
        'total_sales': total_sales,
        'total_receipts': total_receipts,
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'pending_credits': pending_credits,
    }
    return render(request, "kgl_app/managerdashboard.html", context)

def logout(request):
    return redirect('/home/')

@login_required
def addproduct(request, pk=None):
    if not request.user.is_manager:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    if pk:
        issued_product = Product.objects.get(id=pk)
        form = UpdateProductForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                added_quantity = int(request.POST.get('received_quantity'))
                issued_product.total_quantity += added_quantity
                issued_product.save()
                print(added_quantity)
                print(issued_product.total_quantity)
                return redirect('home')
        return render(request, "kgl_app/addproduct.html", {'form': form, 'issued_product': issued_product})
    else:
        form = ProductForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('/products')
        return render(request, "kgl_app/addproduct.html", {'form': form})

@login_required
def creditsales(request):
    if not request.user.is_salesagent:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    if request.method == 'POST':
        form = CreditSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'kgl_app/creditsales.html', {'form': form})
    else:
        form = CreditSaleForm()
    return render(request, "kgl_app/creditsales.html", {'form': form})

@login_required
def creditsaleslist(request):
    if not (request.user.is_salesagent or request.user.is_owner):
        return HttpResponseForbidden("You are not authorized to perform this action.")
    payment = CreditSale.objects.all().order_by('id')
    return render(request, 'kgl_app/creditsaleslist.html', {'payments': payment})

def addsale(request):
    return render(request, "kgl_app/addsale.html")

@login_required
def receipt(request):
    if not request.user.is_owner:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    sales = Sale.objects.all().order_by('id')
    return render(request, "kgl_app/receipt.html", {'sales': sales})

@login_required
def receipt_detail(request, receipt_id):
    if not request.user.is_owner:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    receipt = Sale.objects.get(id=receipt_id)
    return render(request, "kgl_app/receipt_detail.html", {'receipt': receipt})

@login_required
def add_to_stock(request, pk):
    if not request.user.is_manager:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    issued_product = Product.objects.get(id=pk)
    form = AddForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            added_quantity = int(request.POST.get('total_quantity'))
            issued_product.total_quantity += added_quantity
            issued_product.save()
            print(added_quantity)
            print(issued_product.total_quantity)
            return redirect('home')
    return render(request, "kgl_app/add_to_stock.html", {'form': form})

@login_required
def products(request):
    products = Product.objects.all().order_by('id')
    product_filters = ProductFilter(request.GET, queryset=products)
    products = product_filters.qs
    return render(request, "kgl_app/products.html", {'products': products, 'product_filters': product_filters})

def signup(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            return redirect('/login')
    else:
        form = UserCreation()
    return render(request, 'kgl_app/signup.html', {'form': form, 'title': 'Sign Up'})

def save(self, commit=True):
    user = super(UserCreation, self).save(commit=False)
    user.is_salesagent = self.cleaned_data.get('is_salesagent', False)
    user.is_manager = self.cleaned_data.get('is_manager', False)
    user.is_owner = self.cleaned_data.get('is_owner', False)
    if commit:
        user.is_active = True
        user.is_staff = True
        user.save()
    return user


@login_required
def supplier_list(request):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')  # Adjust 'home' to your home URL name
    suppliers = Supplier.objects.all()
    return render(request, 'kgl_app/supplier.html', {'suppliers': suppliers})

@login_required
def supplier_detail(request, supplier_id):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')
    supplier = get_object_or_404(Supplier, id=supplier_id)
    return render(request, 'kgl_app/supplier_detail.html', {'supplier': supplier})

@login_required
def add_supplier(request):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier added successfully!")
            return redirect('supplier')
    else:
        form = SupplierForm()
    return render(request, 'kgl_app/add_supplier.html', {'form': form})

@login_required
def edit_supplier(request, supplier_id):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier updated successfully!")
            return redirect('supplier')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'kgl_app/edit_supplier.html', {'form': form, 'supplier': supplier})

@login_required
def delete_supplier(request, supplier_id):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, "Supplier deleted successfully!")
        return redirect('supplier')
    return render(request, 'kgl_app/delete_supplier.html', {'supplier': supplier})