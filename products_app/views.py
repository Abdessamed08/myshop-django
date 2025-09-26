# products_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from .models import Product, Order, OrderItem, Daira, Commune
from .forms import CheckoutForm
import csv
from django.contrib.auth.decorators import login_required


# 🏠 Pages publiques
#------------------------------------------------------------------------------------------------------------------

def home(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "products_app/home.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'products_app/product_detail.html', {'product': product})


def search_products(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        products = Product.objects.filter(name__icontains=query)[:10]
        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image_url': product.image.url if product.image else '',
            })
    return JsonResponse({'results': results})


def cart_view(request):
    cart = request.session.get("cart", {})
    products = []
    total = 0
    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * qty
        products.append({"product": product, "qty": qty, "subtotal": subtotal})
        total += subtotal
    context = {"cart_items": products, "total": total}
    return render(request, "products_app/cart.html", context)


def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart
    messages.success(request, "Produit ajouté au panier.")
    return redirect(request.META.get('HTTP_REFERER', 'products_app:home'))


def decrease_qty(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]
    request.session["cart"] = cart
    return redirect("products_app:cart")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session["cart"] = cart
    return redirect("products_app:cart")


def clear_cart(request):
    request.session["cart"] = {}
    return redirect("products_app:cart")


def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart
    messages.success(request, f"{product.name} a été ajouté au panier pour achat ✅")
    return redirect("products_app:cart")


@login_required
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Votre panier est vide.")
        return redirect("products_app:cart")
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                wilaya=form.cleaned_data['wilaya'],
                daira=form.cleaned_data['daira'],
                commune=form.cleaned_data['commune'],
                address_details=form.cleaned_data['address_details'],
            )
            for product_id, qty in cart.items():
                product = get_object_or_404(Product, id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price
                )
            request.session["cart"] = {}
            redirect_url = reverse('products_app:order_success', args=[order.id])
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect': redirect_url})
            else:
                messages.success(request, "Votre commande a été confirmée !")
                return redirect(redirect_url)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CheckoutForm(initial={
            'full_name': request.user.get_full_name(),
            'email': request.user.email
        })
    cart_items = []
    total = 0
    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * qty
        cart_items.append({"product": product, "qty": qty, "subtotal": subtotal})
        total += subtotal
    context = {"form": form, "cart_items": cart_items, "total": total}
    return render(request, "products_app/checkout.html", context)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'products_app/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'products_app/order_history.html', {'orders': orders})


def ajax_load_dairas(request):
    wilaya_id = request.GET.get("wilaya_id")
    dairas = Daira.objects.filter(wilaya_id=wilaya_id).values("id", "name")
    return JsonResponse(list(dairas), safe=False)


def ajax_load_communes(request):
    daira_id = request.GET.get("daira_id")
    communes = Commune.objects.filter(daira_id=daira_id).values("id", "name")
    return JsonResponse(list(communes), safe=False)


# 🛠️ Pages admin
#------------------------------------------------------------------------------------------------------------------

@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'products_app/admin_orders.html', {'orders': orders})


@staff_member_required
def export_order_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'User', 'Status', 'Total Amount', 'Created At'])
    orders = Order.objects.all()
    for order in orders:
        writer.writerow([order.id, order.user.username, order.status, order.total_amount, order.created_at])
    return response


@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'products_app/admin_order_detail.html', {'order': order})