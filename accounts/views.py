from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import EditProfileForm, ProfileForm
from .models import Profile # Importer le modèle Profile
from products_app.models import Product, Cart

User = get_user_model()

# ---------------- REGISTER ----------------
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, "accounts/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, "accounts/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, "accounts/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        login(request, user)
        messages.success(request, f"Compte créé avec succès ! Bienvenue {user.username}")
        return redirect("products_app:home")

    return render(request, "accounts/register.html")


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect("products_app:home")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "accounts/login.html")


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    messages.info(request, "Vous êtes maintenant déconnecté.")
    return redirect("accounts:login")


# ---------------- SETTINGS ----------------
@login_required
def settings_view(request):
    return render(request, "accounts/settings.html")


# ---------------- EDIT PROFILE ----------------
@login_required
def edit_profile(request):
    user = request.user
    
    # Correction de l'erreur 'AttributeError'
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        # Crée un profil si l'utilisateur n'en a pas
        profile = Profile.objects.create(user=user)

    if request.method == "POST":
        user_form = EditProfileForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect('accounts:settings')
    else:
        user_form = EditProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, "accounts/edit_profile.html", context)


# ---------------- PASSWORD CHANGE ----------------
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre mot de passe a été changé avec succès !')
            return redirect('accounts:password_change_done')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            
            return render(request, 'accounts/password_change.html', {'form': form})
    else:
        form = PasswordChangeForm(user=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'accounts/password_change.html', context)


# ---------------- PASSWORD CHANGE DONE ----------------
@login_required
def password_change_done(request):
    return render(request, 'accounts/password_change_done.html')


# ---------------- STORE HOME ----------------
def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})


# Add to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    messages.success(request, f"{product.name} a été ajouté au panier ✅")
    return redirect('products_app:home')

# Buy now
@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    cart.save()
    return redirect('products_app:checkout')