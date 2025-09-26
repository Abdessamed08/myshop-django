from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from decimal import Decimal
import csv
from .models import Product, ProductImage, Order, OrderItem, Wilaya, Daira, Commune

# -------------------------
# Inline pour ProductImage
# -------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    can_delete = True
    fields = ('image', 'is_main', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:80px; height:80px; object-fit:cover; border-radius:6px; margin:2px;" />',
                obj.image.url
            )
        return "-"
    preview.short_description = "Aperçu"

    # S'assurer qu'une seule image principale
    def save_model(self, request, obj, form, change):
        if obj.is_main:
            ProductImage.objects.filter(product=obj.product).exclude(pk=obj.pk).update(is_main=False)
        super().save_model(request, obj, form, change)


# -------------------------
# ProductAdmin
# -------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'formatted_price', 'thumbnail', 'is_active', 'images_preview')
    search_fields = ('name',)
    list_per_page = 30
    inlines = [ProductImageInline]
    actions = ['make_inactive', 'make_active']

    def formatted_price(self, obj):
        try:
            return f"{obj.price:,.2f} DA"
        except:
            return "-"
    formatted_price.short_description = "Prix"

    # Miniature image principale
    def thumbnail(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        if main_image:
            return format_html(
                '<img src="{}" style="width:48px; height:48px; object-fit:cover; border-radius:6px;" />',
                main_image.image.url
            )
        return "-"
    thumbnail.short_description = "Image principale"

    # Aperçu de toutes les images
    def images_preview(self, obj):
        imgs = obj.images.all()
        if not imgs:
            return "-"
        html = "".join([
            format_html('<img src="{}" style="width:40px;height:40px;object-fit:cover;border-radius:4px;margin-right:2px;" />', img.image.url)
            for img in imgs
        ])
        return format_html(html)
    images_preview.short_description = "Toutes les images"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Produit(s) désactivé(s) avec succès !")
    make_inactive.short_description = "Désactiver les produits sélectionnés"

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Produit(s) activé(s) avec succès !")
    make_active.short_description = "Activer les produits sélectionnés"


# -------------------------
# Inline OrderItem
# -------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_thumbnail', 'product_link', 'price', 'quantity', 'subtotal_display')
    fields = ('product_thumbnail', 'product_link', 'price', 'quantity', 'subtotal_display')
    show_change_link = True

    def product_thumbnail(self, obj):
        main_image = None
        if getattr(obj, "product", None):
            main_image = obj.product.images.filter(is_main=True).first()
        if main_image:
            return format_html(
                '<img src="{}" style="width:44px; height:44px; object-fit:cover; border-radius:6px;" />',
                main_image.image.url
            )
        return "-"
    product_thumbnail.short_description = "Photo"

    def product_link(self, obj):
        if getattr(obj, "product", None):
            return format_html("<strong>{}</strong>", obj.product.name)
        return "-"
    product_link.short_description = "Produit"

    def subtotal_display(self, obj):
        try:
            subtotal = (obj.price or Decimal('0.00')) * obj.quantity
            return f"{subtotal:,.2f} DA"
        except:
            return "-"
    subtotal_display.short_description = "Sous-total"


# -------------------------
# OrderAdmin
# -------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'status_badge', 'total_display', 'items_count', 'first_item_thumb', 'created_at')
    list_filter = ('status', 'created_at', 'wilaya')
    search_fields = ('user__username', 'full_name', 'email', 'phone', 'address_details')
    inlines = [OrderItemInline]
    actions = ['export_orders_csv']
    list_per_page = 25
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'total_display', 'order_items_summary')

    fieldsets = (
        ('Informations commande', {'fields': ('user', 'status', 'total_display', 'created_at')}),
        ('Détails du client', {'fields': ('full_name', 'email', 'phone')}),
        ('Adresse de livraison', {'fields': ('wilaya', 'daira', 'commune', 'address_details')}),
        ('Récapitulatif des articles (lecture seule)', {'fields': ('order_items_summary',)}),
    )

    def total_display(self, obj):
        total = Decimal('0.00')
        for item in obj.items.all():
            try:
                total += (item.price or Decimal('0.00')) * item.quantity
            except:
                continue
        return f"{total:,.2f} DA"
    total_display.short_description = "Montant total"

    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = "Articles"

    def first_item_thumb(self, obj):
        first = obj.items.first()
        if first and getattr(first.product, 'images', None):
            main_image = first.product.images.filter(is_main=True).first()
            if main_image:
                return format_html(
                    '<img src="{}" style="width:40px; height:40px; object-fit:cover; border-radius:5px;" />',
                    main_image.image.url
                )
        return "-"
    first_item_thumb.short_description = "Aperçu produit"

    def status_badge(self, obj):
        colors = {'pending': '#f59e0b', 'completed': '#16a34a', 'cancelled': '#dc2626'}
        color = colors.get(obj.status, '#374151')
        return format_html(
            '<span style="display:inline-block;padding:2px 8px;border-radius:14px;background:{};color:#fff;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Statut"

    def order_items_summary(self, obj):
        if not obj.pk:
            return "-"
        rows = []
        for item in obj.items.select_related('product').all():
            img_html = "-"
            if getattr(item.product, 'images', None):
                main_image = item.product.images.filter(is_main=True).first()
                if main_image:
                    img_html = format_html(
                        '<img src="{}" style="width:48px;height:48px;object-fit:cover;border-radius:6px;margin-right:8px;" />',
                        main_image.image.url
                    )
            name = item.product.name if item.product else "(produit supprimé)"
            try:
                subtotal = (item.price or Decimal('0.00')) * item.quantity
                subtotal_str = f"{subtotal:,.2f} DA"
            except:
                subtotal_str = "-"
            rows.append(format_html(
                '<div style="display:flex;align-items:center;padding:6px 0;border-bottom:1px solid #eee;">'
                '{}<div style="line-height:1.1;"><strong>{}</strong><br>'
                '<small>Qté: {} — Prix: {} DA — Sous-total: {}</small></div></div>',
                img_html, name, item.quantity, f"{item.price:,.2f}", subtotal_str
            ))
        return format_html(''.join(rows)) if rows else format_html("<em>Aucun article</em>")
    order_items_summary.short_description = "Articles de la commande"

    def export_orders_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="orders_export.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Order ID', 'Utilisateur', 'Nom complet', 'Email', 'Téléphone',
            'Statut', 'Montant total (DA)', 'Wilaya', 'Daira', 'Commune', 'Adresse détaillée',
            'Nb articles', 'Articles détail', 'Date création'
        ])
        for order in queryset:
            total = Decimal('0.00')
            items_desc = []
            for item in order.items.select_related('product').all():
                try:
                    line_sub = (item.price or Decimal('0.00')) * item.quantity
                    total += line_sub
                    pname = item.product.name if item.product else "(produit supprimé)"
                    items_desc.append(f"{item.quantity}x {pname} @ {item.price:,.2f} DA = {line_sub:,.2f} DA")
                except:
                    items_desc.append(f"{item.quantity}x (erreur calcul)")
            writer.writerow([
                order.id,
                order.user.username if order.user else '',
                order.full_name,
                order.email,
                order.phone,
                order.get_status_display(),
                f"{total:,.2f}",
                order.wilaya.name if order.wilaya else '',
                order.daira.name if order.daira else '',
                order.commune.name if order.commune else '',
                order.address_details,
                order.items.count(),
                " | ".join(items_desc),
                order.created_at.strftime("%Y-%m-%d %H:%M:%S")
            ])
        return response
    export_orders_csv.short_description = "Exporter les commandes sélectionnées (CSV)"


# -------------------------
# OrderItemAdmin
# -------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'subtotal_display', 'product_thumb')
    search_fields = ('product__name', 'order__id')
    list_per_page = 40

    def subtotal_display(self, obj):
        try:
            subtotal = (obj.price or Decimal('0.00')) * obj.quantity
            return f"{subtotal:,.2f} DA"
        except:
            return "-"
    subtotal_display.short_description = "Sous-total"

    def product_thumb(self, obj):
        if getattr(obj.product, 'images', None):
            main_image = obj.product.images.filter(is_main=True).first()
            if main_image:
                return format_html(
                    '<img src="{}" style="width:44px;height:44px;object-fit:cover;border-radius:6px;" />',
                    main_image.image.url
                )
        return "-"
    product_thumb.short_description = "Photo Produit"
