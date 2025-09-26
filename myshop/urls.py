# myshop/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # CORRECTION IMPORTANTE : Nous incluons les URLs d'authentification par défaut de Django.
    # Cela enregistre les chemins pour password_reset, password_reset_done, confirm, etc.
    # Ces chemins sont automatiquement nommés par Django et sont nécessaires pour le flux.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # L'inclusion de votre application 'accounts' personnalisée est conservée.
    # Elle contient probablement votre vue d'inscription (register) et éventuellement login/logout
    # personnalisés. Assurez-vous qu'elle utilise le namespace 'accounts' si nécessaire.
    path('accounts/', include('accounts.urls', namespace='accounts')),
    
    path('', include('products_app.urls', namespace='products_app')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)