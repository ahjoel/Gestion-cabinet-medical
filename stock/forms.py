from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.urls import reverse
from django_select2 import forms as s2forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from stock.models import Categorie, Produit, Commande, LigneCommande, Livraison, LigneLivraison, Mouvement, \
    Tarification, Vente, LigneVente


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CategoryForm(forms.ModelForm):
    codeC = forms.CharField(label="Code Catégorie", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nomC = forms.CharField(label="Nom Catégorie", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    descriptC = forms.CharField(label="Description Catégorie", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Categorie
        fields = ['codeC', 'nomC', 'descriptC']


class ProduitForm(forms.ModelForm):
    P = '----------',
    P_U = 'UNITE'
    P_C_10 = 'CARTON 10'
    P_C_20 = 'CARTON 20'
    MES_P = [
        (P, '----------'),
        (P_U, 'UNITE'),
        (P_C_10, 'CARTON 10'),
        (P_C_20, 'CARTON 20'),
    ]
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.filter(disponibleC=True).order_by('-id'), label="Catégorie Produit", required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    codeP = forms.CharField(label="Code Produit", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nomP = forms.CharField(label="Nom Produit", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    descriptP = forms.CharField(label="Description Produit", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mesureP = forms.ChoiceField(label="Mesure Produit", choices=MES_P, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    quantiteMinP = forms.IntegerField(label="Quantité Minimum Produit", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Produit
        fields = ['codeP', 'categorie', 'nomP', 'descriptP', 'quantiteMinP', 'mesureP']


class CommandeForm(forms.ModelForm):
    codeC = forms.CharField(label="Code Commande", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateC = forms.DateField(label="Date Commande", required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Commande
        fields = ['codeC', 'dateC']


class LigneCommandeForm(forms.ModelForm):
    codeC = forms.CharField(label="Code Commande", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateC = forms.DateField(label="Date Commande", required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    produit = forms.ModelChoiceField(queryset=Produit.objects.filter(disponibleP=True).order_by('-id'), label="Produit Commande", required=False, widget=forms.Select(attrs={'class': 'form-control', 'id': 'pdtAdder', 'name': 'pdtAdder'}))
    qte = forms.IntegerField(label="Quantité Commande", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'qteAdder', 'name': 'qte'}))

    class Meta:
        model = LigneCommande
        fields = ['codeC', 'dateC', 'produit', 'qte']


class LivraisonForm(forms.ModelForm):
    codeL = forms.CharField(label="Code Livraison", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fournisseur = forms.CharField(label="Fournisseur", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateL = forms.DateField(label="Date Livraison", required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Livraison
        fields = ['codeL', 'fournisseur', 'dateL']


class LigneLivraisonForm(forms.ModelForm):
    codeL = forms.CharField(label="Code Commande", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateL = forms.DateField(label="Date Commande", required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    fournisseur = forms.CharField(label="Fournisseur", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    commande = forms.ModelChoiceField(queryset=LigneCommande.objects.filter(disponible=True, statut="EN COURS").order_by('-id'), label="Commande", required=False, widget=forms.Select(attrs={'class': 'form-control', 'id': 'cmdAdder', 'name': 'cmdAdder'}))
    produit = forms.ModelChoiceField(queryset=Produit.objects.filter(disponibleP=True).order_by('-id'), label="Produit Livraisé", required=False, widget=forms.Select(attrs={'class': 'form-control', 'id': 'pdtAdder', 'name': 'pdtAdder'}))
    qte = forms.IntegerField(label="Quantité Livrée", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'qteAdder', 'name': 'qte'}))
    prixHt = forms.FloatField(label="Prix Livré", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'prixAdder', 'name': 'prix'}))

    def __init__(self, *args, **kwargs):
        super(LigneLivraisonForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['produit'].disabled = True
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Field('produit', css_class='form-control readonly-field', disabled=True)  # Disable the field
            )

    class Meta:
        model = LigneLivraison
        fields = ['codeL', 'dateL', 'fournisseur', 'commande', 'produit', 'qte', 'prixHt']


class TarificationForm(forms.ModelForm):
    produit = forms.ModelChoiceField(queryset=Produit.objects.filter(disponibleP=True).order_by('-id'), label="Produit",
                                     required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    dateD = forms.DateField(label="Date Début en Vigueur", required=True,
                            widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    dateF = forms.DateField(label="Date de Fin", required=False,
                            widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    prix = forms.FloatField(label="Prix Produit", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Tarification
        fields = ['produit', 'prix', 'dateD', 'dateF']


class MouvementForm(forms.ModelForm):
    class Meta:
        model = Mouvement
        fields = ['dateM', 'produit', 'qte', 'type']


class VenteForm(forms.ModelForm):
    codeV = forms.CharField(label="Code Vente", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    client = forms.CharField(label="Client", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateV = forms.DateField(label="Date Vente", required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    remise = forms.IntegerField(label="Remise", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Vente
        fields = ['codeV', 'client', 'dateV', "remise"]


class LigneVenteForm(forms.ModelForm):
    codeV = forms.CharField(label="Code Vente", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateV = forms.DateField(label="Date Vente", required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}))
    client = forms.CharField(label="Client", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    remise = forms.IntegerField(label="Remise", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    produit = forms.ModelChoiceField(queryset=Produit.objects.filter(disponibleP=True).order_by('-id'), label="Produit Livré", required=False, widget=forms.Select(attrs={'class': 'form-control', 'id': 'pdtAdder', 'name': 'pdtAdder'}))
    qte = forms.IntegerField(label="Quantité Demandée", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'qteAdder', 'name': 'qte'}))
    prix = forms.ModelChoiceField(queryset=Tarification.objects.filter(disponible=True).order_by('-id'), label="Tarif Vigueur", required=False, widget=forms.Select(attrs={'class': 'form-control', 'id': 'prixAdder', 'name': 'prixAdder'}))

    def __init__(self, *args, **kwargs):
        super(LigneVenteForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['produit'].disabled = True
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Field('produit', css_class='form-control readonly-field', disabled=True)  # Disable the field
            )

    class Meta:
        model = LigneVente
        fields = ['codeV', 'dateV', 'client', 'remise', 'produit', 'qte', 'prix']

