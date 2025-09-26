# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """
    Modèle d'utilisateur personnalisé.
    """
    groups = models.ManyToManyField(
        Group,
        related_name='accounts_users',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_query_name='accounts_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='accounts_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='accounts_user',
    )


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    photo = models.ImageField(
        upload_to='profiles/',
        default='profiles/default_profile.png',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    dark_mode = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


# Signal pour créer ou mettre à jour un profil utilisateur automatiquement
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Gère les cas où un profil n'existe pas encore pour un utilisateur existant
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)
        # Si le profil existe, on le sauvegarde.
        # Note : En général, il n'est pas nécessaire de sauvegarder le profil ici,
        # car la vue s'en occupe. Je le laisse pour être exhaustif.
        else:
            instance.profile.save()