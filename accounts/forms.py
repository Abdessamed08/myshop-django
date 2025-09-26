from django import forms
# Importez AbstractUser depuis le modèle de Django, si nécessaire,
# et votre modèle User personnalisé depuis votre propre fichier models.py
from .models import Profile, User 

# Supprimez cette ligne : from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm # Importation de la classe de base pour l'édition d'utilisateur

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Prénom"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom"}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["photo", "bio", "phone"]
        widgets = {
            "photo": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),
            "bio": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Écris une courte présentation..."
            }),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Numéro de téléphone"}),
        }