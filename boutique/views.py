from django.shortcuts import render
from .models import Produit

def home(request):
    produits = Produit.objects.all()
    return render(request, 'home.html', {'produits': produits})

