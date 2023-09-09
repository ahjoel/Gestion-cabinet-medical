from django.contrib.auth.models import User
from django.db import models


class Categorie(models.Model):
    auteurC = models.ForeignKey(User, on_delete=models.PROTECT)
    codeC = models.CharField(max_length=10, blank=False, null=False, unique=True)
    nomC = models.CharField(max_length=30, blank=False, null=False, unique=True)
    descriptC = models.CharField(max_length=80)
    disponibleC = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nomC


class Produit(models.Model):
    P_U = 'UNITE'
    P_C_10 = 'CARTON 10'
    P_C_20 = 'CARTON 20'
    MES_P = [
        (P_U, 'UNITE'),
        (P_C_10, 'CARTON 10'),
        (P_C_20, 'CARTON 20'),
    ]
    auteurP = models.ForeignKey(User, on_delete=models.PROTECT)
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT,)
    codeP = models.CharField(max_length=10, blank=False, null=False, unique=True)
    nomP = models.CharField(max_length=30, blank=False, null=False, unique=True)
    descriptP = models.CharField(max_length=80)
    disponibleP = models.BooleanField(default=True)
    quantiteMinP = models.PositiveIntegerField()
    mesureP = models.CharField(max_length=30, choices=MES_P, default='', blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.codeP + " " + self.nomP + " " + self.mesureP


class CommandeConsultant(models.Model):
    EN_COURS = 'EN COURS'
    TRAITEE = 'TRAITEE'
    NON_DISPO = 'PDT RUPTURE STOCK'
    CHOIX = [
        (EN_COURS, 'EN COURS'),
        (TRAITEE, 'TRAITEE'),
        (NON_DISPO, 'PDT RUPTURE STOCK'),
    ]
    auteurC = models.ForeignKey(User, on_delete=models.PROTECT, related_name="autheur_consul")
    auteurT = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name="autheur_admin")
    codeC = models.CharField(max_length=100, blank=False, null=False, unique=True)
    dateC = models.DateField()
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    qte = models.IntegerField()
    disponible = models.BooleanField(default=True)
    statut = models.CharField(max_length=30, choices=CHOIX, default=EN_COURS)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.codeC

class Commande(models.Model):
    auteurC = models.ForeignKey(User, on_delete=models.PROTECT)
    codeC = models.CharField(max_length=100, blank=False, null=False, unique=True)
    dateC = models.DateField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.codeC


class LigneCommande(models.Model):
    EN_COURS = 'EN COURS'
    LIVREE = 'LIVREE'
    CHOIX = [
        (EN_COURS, 'EN COURS'),
        (LIVREE, 'LIVREE'),
    ]
    auteurC = models.ForeignKey(User, on_delete=models.PROTECT)
    commande = models.ForeignKey(Commande, on_delete=models.PROTECT)
    statut = models.CharField(max_length=15, choices=CHOIX, default=EN_COURS)
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    qte = models.IntegerField()
    disponible = models.BooleanField(default=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.commande.codeC + " " + self.produit.nomP)


class Livraison(models.Model):
    auteurL = models.ForeignKey(User, on_delete=models.PROTECT)
    codeL = models.CharField(max_length=100, blank=False, null=False, unique=True)
    dateL = models.DateField()
    fournisseur = models.CharField(max_length=100, blank=False, null=False, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.codeL


class LigneLivraison(models.Model):
    NON_VA = 'NON-VA'
    VA = 'VA'
    CHOIX = [
        (NON_VA, 'NON-VA'),
        (VA, 'VA'),
    ]
    auteurL = models.ForeignKey(User, on_delete=models.PROTECT)
    livraison = models.ForeignKey(Livraison, on_delete=models.PROTECT)
    commande = models.ForeignKey(LigneCommande, on_delete=models.PROTECT)
    statut = models.CharField(max_length=15, choices=CHOIX, default=NON_VA)
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    qte = models.IntegerField()
    prixHt = models.FloatField()
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.livraison)


class Tarification(models.Model):
    ACTUELLE = 'ACTUELLE'
    OBSOLETE = 'OBSOLETE'
    CHOIX = [
        (ACTUELLE, 'ACTUELLE'),
        (OBSOLETE, 'OBSOLETE'),
    ]
    NON_VA = 'NON-VA'
    VA = 'VA'
    CHOIX_S = [
        (NON_VA, 'NON-VA'),
        (VA, 'VA'),
    ]
    auteurT = models.ForeignKey(User, on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    prix = models.FloatField()
    dateD = models.DateField()
    dateF = models.DateField(null=True, blank=True)
    vigeur = models.CharField(max_length=15, choices=CHOIX, default=ACTUELLE)
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.prix)


class Vente(models.Model):
    auteurV = models.ForeignKey(User, on_delete=models.PROTECT)
    codeV = models.CharField(max_length=100, blank=False, null=False, unique=True)
    dateV = models.DateField()
    client = models.CharField(max_length=100, blank=False, null=False, unique=True)
    remise = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.codeV


class LigneVente(models.Model):
    NON_VA = 'NON-VA'
    VA = 'VA'
    CHOIX = [
        (NON_VA, 'NON-VA'),
        (VA, 'VA'),
    ]
    auteurL = models.ForeignKey(User, on_delete=models.PROTECT)
    vente = models.ForeignKey(Vente, on_delete=models.PROTECT)
    tarification = models.ForeignKey(Tarification, on_delete=models.PROTECT)
    statut = models.CharField(max_length=15, choices=CHOIX, default=NON_VA)
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    qte = models.IntegerField()
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.vente)


class Mouvement(models.Model):
    auteurM = models.ForeignKey(User, on_delete=models.PROTECT)
    dateM = models.DateField()
    llivraison = models.ForeignKey(LigneLivraison, on_delete=models.PROTECT, null=True)
    sortie = models.ForeignKey(LigneVente, on_delete=models.PROTECT, null=True)
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    qte = models.IntegerField()
    IN = 'IN'
    OUT = 'OUT'
    CHOIX_MOUVEMENT = [
        (IN, 'IN'),
        (OUT, 'OUT'),
    ]
    type = models.CharField(
        max_length=8,
        choices=CHOIX_MOUVEMENT,
        default="",
    )
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.produit
