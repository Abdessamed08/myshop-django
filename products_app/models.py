from django.db import models
from django.conf import settings   # ✅ utiliser AUTH_USER_MODEL
from django.db.models.signals import post_delete
from django.dispatch import receiver

# 🔹 Produit
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # image principale
    is_active = models.BooleanField(default=True)  # ✅ pour soft delete

    def __str__(self):
        return self.name

    # ✅ Méthode pour soft delete
    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

# 🔹 Images supplémentaires d’un produit (avec image principale possible)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    is_main = models.BooleanField(default=False)  # Indique si c’est l’image principale

    def __str__(self):
        return f"Image de {self.product.name}"

# 🔹 Panier
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ corrigé
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f"Panier de {self.user.username}"

    def total_price(self):
        return sum(product.price for product in self.products.filter(is_active=True))  # seulement actifs

# 🔹 Commande
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ corrigé
    full_name = models.CharField(max_length=100, default="Nom non défini")
    email = models.EmailField(default="email@exemple.com")
    phone = models.CharField(max_length=20, blank=True)
    wilaya = models.ForeignKey('Wilaya', on_delete=models.PROTECT, null=True, blank=True)
    daira = models.ForeignKey('Daira', on_delete=models.PROTECT, null=True, blank=True)
    commune = models.ForeignKey('Commune', on_delete=models.PROTECT, null=True, blank=True)
    address_details = models.TextField(default="Adresse détaillée non définie")
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Commande {self.id} - {self.user.username}"

# 🔹 Articles d’une commande
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.price * self.quantity

# 🔹 Wilayas, Dairas et Communes (Algérie)
class Wilaya(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Daira(models.Model):
    name = models.CharField(max_length=100)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} ({self.wilaya.name})"

class Commune(models.Model):
    name = models.CharField(max_length=100)
    daira = models.ForeignKey(Daira, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} ({self.daira.name})"

# 🔹 Suppression des fichiers image sur disque
@receiver(post_delete, sender=ProductImage)
def delete_product_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)

@receiver(post_delete, sender=Product)
def delete_product_main_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)
