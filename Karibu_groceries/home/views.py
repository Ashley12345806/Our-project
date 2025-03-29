from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def sales(request):
    return render(request, 'sales.html')

def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def products(request):
    return render(request, 'products.html')

def logout(request):
    return render(request, 'logout.html')