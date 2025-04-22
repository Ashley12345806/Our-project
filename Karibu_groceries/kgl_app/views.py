from django.shortcuts import render
from kgl_app.models import *


# Create your views here.
def index(request):
    return render(request, "kgl_app/home.html")


def home(request):
    #get all products from the database and order them by id
    products = Product.objects.all().order_by('id')
    return render(request, "kgl_app/index.html", {'products': products})

def sales(request):
    return render(request, "kgl_app/sales.html")

def signup(request):
    return render(request, "kgl_app/signup.html")


def login(request):
    return render(request, "kgl_app/login.html")

def dashboard(request):
    return render(request, "kgl_app/dashboard.html")


def logout(request):
    return render(request, "kgl_app/logout.html")


def addproduct(request):
    return render(request, "kgl_app/addproduct.html")


def deferredpayment(request):
    payment = Deffered_payment.objects.all()
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        nin = request.POST.get('nin')
        product_name = request.POST.get('product_name')
        amount = request.POST.get('amount')
        balance = request.POST.get('balance')
        duedate = request.POST.get('duedate')
        date_of_payment = request.POST.get('date_of_payment')
        branch = request.POST.get('branch')
        sales_agent = request.POST.get('sales_agent')

        Deffered_payment.objects.create(
            customer_name=customer_name,
            contact=contact,
            address=address,
            nin=nin,
            product_name=product_name,
            amount=amount,
            balance=balance,
            duedate=duedate,
            date_of_payment=date_of_payment,
            branch=branch,
            sales_agent=sales_agent
        )
    return render(request, "kgl_app/deferredpayment.html" , {'payment': payment})

def deferredpaymentlist(request):
    return render(request, 'kgl_app/deferredpaymentlist.html')


def addsale(request):
    return render(request, "kgl_app/addsale.html")

def receipt(request):
    return render(request, "kgl_app/receipt.html")


