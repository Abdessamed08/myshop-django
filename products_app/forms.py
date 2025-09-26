# forms.py
from django import forms
from .models import Order, Wilaya, Daira, Commune

class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        label="Nom complet",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet', 'required': 'required'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre adresse email', 'required': 'required'})
    )
    phone = forms.CharField(
        label="Téléphone",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre numéro de téléphone', 'required': 'required'})
    )

    wilaya = forms.ModelChoiceField(
        queryset=Wilaya.objects.all(),
        label="Wilaya *",
        empty_label="-- Sélectionner une wilaya --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    daira = forms.ModelChoiceField(
        queryset=Daira.objects.none(),
        label="Daira *",
        empty_label="-- Sélectionner une daira --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    commune = forms.ModelChoiceField(
        queryset=Commune.objects.none(),
        label="Commune *",
        empty_label="-- Sélectionner une commune --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    address_details = forms.CharField(
        label="Adresse détaillée",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Rue, numéro, immeuble, etc.', 'rows': 3, 'required': 'required'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mettre à jour dynamiquement le queryset des champs daira et commune
        if 'wilaya' in self.data:
            try:
                wilaya_id = int(self.data.get('wilaya'))
                self.fields['daira'].queryset = Daira.objects.filter(wilaya_id=wilaya_id).order_by('name')
            except (ValueError, TypeError):
                pass
        
        if 'daira' in self.data:
            try:
                daira_id = int(self.data.get('daira'))
                self.fields['commune'].queryset = Commune.objects.filter(daira_id=daira_id).order_by('name')
            except (ValueError, TypeError):
                pass

        # Gérer les labels d'instance
        self.fields['wilaya'].label_from_instance = lambda obj: f"{obj.id} - {obj.name}"
        self.fields['daira'].label_from_instance = lambda obj: f"{obj.name}"
        self.fields['commune'].label_from_instance = lambda obj: f"{obj.name}"
        
        # Le formulaire est-il posté ?
        is_posted = self.is_bound and self.is_valid()
        
        # Rendre les champs obligatoires
        self.fields['daira'].required = True
        self.fields['commune'].required = True