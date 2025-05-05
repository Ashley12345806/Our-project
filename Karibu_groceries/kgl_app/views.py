from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from .filters import ProductFilter
from .models import *
from .forms import *
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, "kgl_app/index.html")


def index(request):
    products = Product.objects.all().order_by('id')
    return render(request, "kgl_app/home.html", {'products': products})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if (request.user.is_manager or request.user.is_salesagent) and product.branch != request.user.branch:
        return HttpResponseForbidden("You are not authorized to view this product.")
    return render(request, 'kgl_app/productdetail.html', {'product': product})


@login_required
def delete_product(request, product_id):
    if not request.user.is_manager:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    product = get_object_or_404(Product, id=product_id)
    if product.branch != request.user.branch:
        return HttpResponseForbidden("You are not authorized to delete this product.")
    product.delete()
    return HttpResponseRedirect(reverse('products'))


@login_required
def edit_product(request, product_id):
    if not request.user.is_manager:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    product = get_object_or_404(Product, id=product_id)
    if product.branch != request.user.branch:
        return HttpResponseForbidden("You are not authorized to edit this product.")
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
    issued_product = get_object_or_404(Product, id=pk)
    if issued_product.branch != request.user.branch:
        return HttpResponseForbidden("You are not authorized to issue this product.")
    
    sales_form = SaleForm(request.user, request.POST or None)
    if request.method == 'POST':
        if sales_form.is_valid():
            issued_quantity = int(request.POST['quantity'])  # Quantity requested by the user
            
            # Check if there is enough stock
            if issued_product.total_quantity < issued_quantity:
                messages.error(request, f"Insufficient stock! Only {issued_product.total_quantity} units of {issued_product.product_name} are available.")
                return render(request, "kgl_app/issue_item.html", {'sales_form': sales_form, 'issued_product': issued_product})
            
            # Calculate the total sale value
            total_sale_value = issued_quantity * issued_product.unit_price
            
            # Check if the total sale value is less than 5000
            if total_sale_value < 5000:
                messages.error(request, f"Sale value must be at least 5000. Current sale value is {total_sale_value}.")
                return render(request, "kgl_app/issue_item.html", {'sales_form': sales_form, 'issued_product': issued_product})
            
            # Proceed with the sale if both conditions are met
            new_sale = sales_form.save(commit=False)
            new_sale.product = issued_product.product_name
            new_sale.unit_price = issued_product.unit_price
            new_sale.branch = issued_product.branch  # Ensure the sale is linked to the correct branch
            new_sale.salesagent = request.user.username  # Record the sales agent
            new_sale.save()
            
            # Update the stock quantity
            issued_product.total_quantity -= issued_quantity
            issued_product.save()
            
            messages.success(request, f"Successfully sold {issued_quantity} units of {issued_product.product_name} for {total_sale_value}.")
            return redirect('products')  # This ensures redirection to the products page
    return render(request, "kgl_app/issue_item.html", {'sales_form': sales_form, 'issued_product': issued_product})


@login_required
def sales(request):
    if not (request.user.is_owner or request.user.is_manager):
        return HttpResponseForbidden("You are not authorized to perform this action.")
    if request.user.is_owner:
        sales = Sale.objects.all().order_by('id')
    else:
        sales = Sale.objects.filter(branch=request.user.branch).order_by('id')
    total_expected = sum([sale.get_total() or 0 for sale in sales])
    total = sum([sale.amount_received or 0 for sale in sales])
    total_change = sum([sale.get_change() or 0 for sale in sales])
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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_owner:
                    return redirect('dashboard')
                elif user.is_salesagent:
                    return redirect('products')
                elif user.is_manager:
                    return redirect('managerdashboard')
            messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'kgl_app/login.html', {'form': form, 'title': 'Login'})


@login_required
def dashboard(request):
    if not request.user.is_owner:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    total_sales = Sale.objects.aggregate(total=Sum('amount_received'))['total'] or 0
    total_receipts = Sale.objects.count()
    total_products = Product.objects.count()
    total_branches = Branch.objects.count()
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
    branch = request.user.branch
    if not branch:
        return HttpResponseForbidden("No branch assigned to this manager.")
    total_sales = Sale.objects.filter(branch=branch).aggregate(total=Sum('amount_received'))['total'] or 0
    total_receipts = Sale.objects.filter(branch=branch).count()
    total_products = Product.objects.filter(branch=branch).count()
    total_suppliers = Supplier.objects.filter(branch=branch).count()
    pending_credits = CreditSale.objects.filter(branch=branch).count()
    context = {
        'user': request.user,
        'branch': branch,
        'total_sales': total_sales,
        'total_receipts': total_receipts,
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'pending_credits': pending_credits,
    }
    return render(request, "kgl_app/managerdashboard.html", context)


def Logout(request):
    logout(request)
    return redirect('home')


@login_required
def addproduct(request, pk=None):
    if not request.user.is_manager:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    if pk:
        issued_product = get_object_or_404(Product, id=pk)
        if issued_product.branch != request.user.branch:
            return HttpResponseForbidden("You are not authorized to update this product.")
        form = UpdateProductForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                added_quantity = int(request.POST.get('received_quantity'))
                issued_product.total_quantity += added_quantity
                issued_product.save()
                return redirect('home')
        return render(request, "kgl_app/addproduct.html", {'form': form, 'issued_product': issued_product})
    else:
        form = ProductForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                product = form.save(commit=False)
                product.branch = request.user.branch
                product.save()
                return redirect('products')
        return render(request, "kgl_app/addproduct.html", {'form': form})


@login_required
def creditsales(request):
    if not request.user.is_salesagent:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    if request.method == 'POST':
        form = CreditSaleForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'kgl_app/creditsales.html', {'form': form})
    else:
        form = CreditSaleForm(request.user)
    return render(request, "kgl_app/creditsales.html", {'form': form})


@login_required
def creditsaleslist(request):
    if not (request.user.is_salesagent or request.user.is_owner or request.user.is_manager):
        return HttpResponseForbidden("You are not authorized to perform this action.")
    branch = request.user.branch
    if not branch and not request.user.is_owner:
        return HttpResponseForbidden("No branch assigned to this user.")
    if request.user.is_owner:
        payments = CreditSale.objects.all().order_by('id')
    else:
        payments = CreditSale.objects.filter(branch=branch).order_by('id')
    return render(request, 'kgl_app/creditsaleslist.html', {'payments': payments})


def addsale(request):
    return render(request, "kgl_app/addsale.html")


@login_required
def receipt(request):
    if not (request.user.is_owner or request.user.is_manager):
        return HttpResponseForbidden("You are not authorized to perform this action.")
    if request.user.is_owner:
        sales = Sale.objects.all().order_by('id')
    else:
        sales = Sale.objects.filter(branch=request.user.branch).order_by('id')
    return render(request, "kgl_app/receipt.html", {'sales': sales})


@login_required
def receipt_detail(request, receipt_id):
    if not (request.user.is_owner or request.user.is_manager):
        return HttpResponseForbidden("You are not authorized to perform this action.")
    receipt = get_object_or_404(Sale, id=receipt_id)
    if not request.user.is_owner and receipt.branch != request.user.branch:
        return HttpResponseForbidden("You are not authorized to view this receipt.")
    return render(request, "kgl_app/receipt_detail.html", {'receipt': receipt})


@login_required
def add_to_stock(request, pk):
    if not request.user.is_manager:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    issued_product = get_object_or_404(Product, id=pk)
    if issued_product.branch != request.user.branch:
        return HttpResponseForbidden("You are not authorized to update this product.")
    form = AddForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            added_quantity = int(request.POST.get('total_quantity'))
            issued_product.total_quantity += added_quantity
            issued_product.save()
            return redirect('home')
    return render(request, "kgl_app/add_to_stock.html", {'form': form})


@login_required
def products(request):
    if request.user.is_owner:
        products = Product.objects.all().order_by('id')
    else:
        products = Product.objects.filter(branch=request.user.branch).order_by('id')
    product_filters = ProductFilter(request.GET, queryset=products)
    products = product_filters.qs
    return render(request, "kgl_app/products.html", {'products': products, 'product_filters': product_filters})

def signup(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = UserCreation()
    return render(request, 'kgl_app/signup.html', {'form': form, 'title': 'Sign Up'})


@login_required
def supplier_list(request):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')
    suppliers = Supplier.objects.filter(branch=request.user.branch)
    return render(request, 'kgl_app/supplier.html', {'suppliers': suppliers})


@login_required
def supplier_detail(request, supplier_id):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if supplier.branch != request.user.branch:
        return HttpResponseForbidden("You are not authorized to view this supplier.")
    return render(request, 'kgl_app/supplier_detail.html', {'supplier': supplier})


@login_required
def add_supplier(request):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.branch = request.user.branch
            supplier.save()
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
    if supplier.branch != request.user.branch:
        return HttpResponseForbidden("You are not authorized to edit this supplier.")
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
    if supplier.branch != request.user.branch:
        return HttpResponseForbidden("You are not authorized to delete this supplier.")
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, "Supplier deleted successfully!")
        return redirect('supplier')
    return render(request, 'kgl_app/delete_supplier.html', {'supplier': supplier})

