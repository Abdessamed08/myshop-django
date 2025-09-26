from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, "products_app/home.html", {"products": products})
