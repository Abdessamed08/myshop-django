from django.urls import path
from . import views

app_name = "products_app"

urlpatterns = [
    # Pages publiques
    path("", views.home, name="home"),
    path("cart/", views.cart_view, name="cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("decrease-qty/<int:product_id>/", views.decrease_qty, name="decrease_qty"),
    path("remove-from-cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("clear-cart/", views.clear_cart, name="clear_cart"),
    path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),
    path("checkout/", views.checkout, name="checkout"),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path("ajax/load-dairas/", views.ajax_load_dairas, name="ajax_load_dairas"),
    path("ajax/load-communes/", views.ajax_load_communes, name="ajax_load_communes"),
    path('orders/', views.order_history, name='order_history'),

    # Admin : gestion des commandes
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/export_orders_csv/', views.export_order_csv, name='export_orders_csv'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search'),

    # Si tu veux afficher les détails d'une commande admin, tu peux décommenter cette ligne après avoir créé la vue
    # path('admin/orders/<int:order_id>/', views.order_detail, name='order_detail'),
]
