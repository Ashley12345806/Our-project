from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .filters import ProductFilter
#access the models in the database
from kgl_app.models import *
from kgl_app.forms import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request, "kgl_app/index.html")


def index(request):
    #get all products from the database and order them by id
    products = Product.objects.all().order_by('id')
    return render(request, "kgl_app/home.html", {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'kgl_app/productdetail.html', {'product': product})


@login_required
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return HttpResponseRedirect(reverse('products'))

@login_required
def issue_item(request, pk):
    #accessing products from the stock model
    issued_product = Product.objects.get(id=pk)
    #accessing our form
    sales_form = SaleForm(request.POST )
    if request.method == 'POST':
        #checking if the form is valid
        if sales_form.is_valid():
            new_sale = sales_form.save(commit = False)
            new_sale.product = issued_product.product_name
            new_sale.unit_price = issued_product.unit_price
            new_sale.save()
            #keep track of sales reamaining after sales
            issued_quantity =int(request.POST['quantity'])
            issued_product.total_quantity -=  issued_quantity
            issued_product.save()


            return redirect('receipt')
    return render(request, "kgl_app/issue_item.html", {'sales_form': sales_form})    

   


def sales(request):
    sales = Sale.objects.all().order_by('id')
    total_expected = sum([products.get_total() or 0 for products in sales])
    total = sum([products.amount_received or 0 for products in sales])
    total_change = sum([products.get_change() or 0 for products in sales])
    net = total_expected - total
    return render(request, "kgl_app/sales.html",{'sales': sales, 'total_expected': total_expected, 'total': total, 'total_change': total_change, 'net': net})


#view for Login page
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #checking in login user
        user = authenticate(request, username=username, password=password)
        #checking if user is owner
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
    total_sales = Sale.objects.aggregate(total=Sum('amount_received'))['total'] or 0
    total_receipts = Sale.objects.count()
    total_products = Product.objects.count()
    total_branches = Product.objects.values('branch_name').distinct().count()

    context = {
        'total_sales': total_sales,
        'total_receipts': total_receipts,
        'total_products': total_products,
        'total_branches': total_branches,
    }
    return render(request, 'kgl_app/dashboard.html', context)

@login_required
def managerdashboard(request):
    total_sales = Sale.objects.aggregate(total=Sum('amount_received'))['total'] or 0
    total_receipts = Sale.objects.count()  # each sale is a receipt
    total_products = Product.objects.count()

    context = {
        'total_sales': total_sales,
        'total_receipts': total_receipts,
        'total_products': total_products,
    }
    return render(request, "kgl_app/managerdashboard.html", context)



def logout(request):
    return render(request, "kgl_app/logout.html")


def addproduct(request, pk):
    issued_product = Product.objects.get(id=pk)
    #accessing our form
    form = UpdateProductForm(request.POST)
    if request.method == 'POST':
        #checking if the form is valid
        if form.is_valid():
            added_quantity = int(request.POST.get('received_quantity'))
            issued_product.total_quantity += added_quantity
            issued_product.save()
            #to add the remaining quantity to the stock
            print(added_quantity)
            print(issued_product.total_quantity)
            return redirect('home')
    return render(request, "kgl_app/addproduct.html", {'form': form, 'issued_product': issued_product})

@login_required
def deferredpayment(request):
  if request.method == 'POST':
       form = DefferedPaymentForm(request.POST)
       if form.is_valid():
           form.save()
           # Redirect on successful form submission
           return redirect('home')
       else:
         # If the form is not valid, return the form with errors
           return render(request, 'kgl_app/deferredpayment.html', {'form': form})
  else:
         form = DefferedPaymentForm()
# Always return a response in case of GET request or invalid form
  return render(request, "kgl_app/deferredpayment.html" , {'form': form})

@login_required
def deferredpaymentlist(request):
    payment = Deffered_payment.objects.all().order_by('id')
    return render(request, 'kgl_app/deferredpaymentlist.html', {'payments': payment})


def addsale(request):
    return render(request, "kgl_app/addsale.html")



def receipt(request):
    sales = Sale.objects.all().order_by('id')
    return render(request, "kgl_app/receipt.html", {'sales': sales})

def receipt_detail(request, receipt_id):
    receipt = Sale.objects.get(id=receipt_id)
    return render(request, "kgl_app/receipt_detail.html", {'receipt': receipt})


def add_to_stock(request,pk):
    issued_product = Product.objects.get(id=pk)
    form = AddForm(request.POST)
    if request.method == 'POST':
        #checking if the form is valid
        if form.is_valid():
            added_quantity = int(request.POST.get('total_quantity'))
            issued_product.total_quantity += added_quantity
            issued_product.save()
            #to add the remaining quantity to the stock
            print(added_quantity)
            print(issued_product.total_quantity)
            return redirect('home')
    return render(request, "kgl_app/add_to_stock.html", {'form': form})

def products(request):
    products = Product.objects.all().order_by('id')
    # Filter products based on the search query if it exists
    product_filters =ProductFilter(request.GET, queryset=products)
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



