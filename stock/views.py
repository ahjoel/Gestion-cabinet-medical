import os
from datetime import date, datetime


from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import F, Sum, ExpressionWrapper, DecimalField, IntegerField
from django.db.models.functions import Cast


from core import settings
from .utils import render_to_pdf
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.views import View
from django.http import *
from stock.forms import RegisterForm, CategoryForm, ProduitForm, LigneCommandeForm, LigneLivraisonForm, \
    TarificationForm, LigneVenteForm
from stock.models import Categorie, Produit, Commande, LigneCommande, LigneLivraison, Livraison, Mouvement, \
    Tarification, Vente, LigneVente


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


@login_required(login_url="/login")
def home(request):
    # users_with_group = User.objects.annotate(group_name=models.F('groups__name'))
    # user_data = users_with_group.filter(id=request.user.id).values('username', 'is_staff', 'group_name').first()
    total_ht = LigneVente.objects.filter(disponible=True).aggregate(
        total_ht=ExpressionWrapper(
            Sum(F('qte') * F('tarification__prix') * 1.18),
            output_field=IntegerField(),
        )
    )['total_ht']
    total_products_count = Produit.objects.filter(disponibleP=True).count()
    produitcommandes = LigneCommande.objects.filter(disponible=True).count()
    produitcommandes_livre = LigneCommande.objects.filter(disponible=True, statut="LIVREE").count()
    mouvements = Mouvement.objects.filter(disponible=True).order_by('-id')

    context = {
        "total_ht": total_ht,
        "total_products_count": total_products_count,
        "produitcommandes": produitcommandes,
        "produitcommandes_livre": produitcommandes_livre,
        "mouvements": mouvements
    }
    return render(request, 'accueil/accueil.html', context)


@login_required(login_url="/login")
def categories(request):
    categories = Categorie.objects.filter(disponibleC=True).order_by('-id')
    return render(request, 'categorie/categories.html', {"categories": categories})


@login_required(login_url="/login")
def create_category(request):
    titre = "Enregistrement"
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.auteurC = request.user
            category.save()
            messages.success(request, "Enregistrement effectué", extra_tags='custom-success')
            return redirect("/create-categorie")
    else:
        form = CategoryForm()
    return render(request, 'categorie/categorie_form.html',  {"form": form, "titre": titre})


@login_required(login_url="/login")
def update_category(request, id):
    titre = "Modification"
    category = get_object_or_404(Categorie, id=id)
    form = CategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée", extra_tags='custom-success')
        return redirect('/categories')

    return render(request, 'categorie/categorie_form.html', {'form': form, "titre": titre})


@login_required(login_url="/login")
def delete_category(request, id):
    category = get_object_or_404(Categorie, id=id)

    if category:
        category.disponibleC = False
        category.save()
        messages.success(request, "Suppression effectuée", extra_tags='custom-success')
        return redirect('/categories')

    return render(request, 'categorie/categories.html', {'category': category})


@login_required(login_url="/login")
def produits(request):
    produits = Produit.objects.filter(disponibleP=True).order_by('-id')
    return render(request, 'produit/produits.html', {"produits": produits})


@login_required(login_url="/login")
def create_produit(request):
    titre = "Enregistrement"
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.auteurP = request.user
            produit.save()
            messages.success(request, "Enregistrement effectué", extra_tags='custom-success')
            return redirect("/create-produit")
    else:
        form = ProduitForm()
    return render(request, 'produit/produit_form.html',  {"form": form, "titre": titre})


@login_required(login_url="/login")
def update_produit(request, id):
    titre = "Modification"
    produit = get_object_or_404(Produit, id=id)
    form = ProduitForm(request.POST or None, instance=produit)

    if form.is_valid():
        form.save()
        messages.success(request, "Modification effectuée", extra_tags='custom-success')
        return redirect('/produits')

    return render(request, 'produit/produit_form.html', {'form': form, "titre": titre})


@login_required(login_url="/login")
def delete_produit(request, id):
    produit = get_object_or_404(Produit, id=id)

    if produit:
        produit.disponibleP = False
        produit.save()
        messages.success(request, "Suppression effectuée", extra_tags='custom-success')
        return redirect('/produits')

    return render(request, 'produit/produits.html', {'produit': produit})


@login_required(login_url="/login")
def listCommande(request):
    produitcommandes = LigneCommande.objects.filter(disponible=True).order_by('-id')
    return render(request, 'produitCommande/produitcommande.html', {"produitcommandes": produitcommandes})


@login_required(login_url="/login")
def create_listcommande(request):
    titre = "Enregistrement"
    form = LigneCommandeForm(request.POST or None)
    d = date.today().strftime("%d%m%Y")
    id_max = Commande.objects.all().count()
    if (id_max == 0):
        id_max = 1
    else:
        id_max = id_max + 1
    ref_com = "CMD0" + str(d) + str(id_max)

    if request.method=='POST':
        date_com = request.POST['dateC']
        ref_com = request.POST['codeC']
        pdt = request.POST.getlist('pdtIds[]')
        qte = request.POST.getlist('qtePdt[]')
        if (pdt):
            com = Commande.objects.create(codeC=ref_com, dateC=date_com, auteurC=request.user)
            commande_id = com.id
            for i in range(len(pdt)):
                LigneCommande.objects.create(commande=Commande.objects.get(pk=commande_id), produit=Produit.objects.get(pk=pdt[i]), qte=qte[i], auteurC=request.user)

            messages.success(request, "Enregistrement(s) effectué(s)", extra_tags='custom-success')
            return redirect('lcommandes')
        else:
            messages.warning(request, "Svp, Veuillez enregistrer au moins une ligne commande de produit.", extra_tags='custom-warning')
            return render(request, 'produitCommande/produitcommande_form.html', {'form': form, 'codeC': ref_com, "titre": titre})

    return render(request, 'produitCommande/produitcommande_form.html', {'form': form, 'codeC': ref_com, "titre": titre})


@login_required(login_url="/login")
def update_lignecommande(request, id):
    titre = "Modification"
    com = get_object_or_404(LigneCommande, id=id)
    form = LigneCommandeForm(request.POST or None, instance=com)

    if request.method=='POST':
        produit = request.POST['produit']
        qte = request.POST['qte']
        com.produit = Produit.objects.get(pk=produit)
        com.qte = qte
        com.save()
        messages.success(request, "Modification effectuée", extra_tags='custom-success')
        return redirect('lcommandes')

    return render(request, 'produitCommande/produitcommande_forms.html', {'form': form, "titre": titre, "com": com})


@login_required(login_url="/login")
def delete_lignecommande(request, id):
    produitc = get_object_or_404(LigneCommande, id=id)

    if produitc:
        produitc.disponible = False
        produitc.save()
        messages.success(request, "Suppression effectuée", extra_tags='custom-success')
        return redirect('/lcommandes')

    return render(request, 'produitCommande/produitcommande.html', {'produitc': produitc})


@login_required(login_url="/login")
def listLivraison(request):
    query = """
                select stock_lignelivraison.id, stock_commande."codeC", 
                stock_livraison.fournisseur, stock_livraison."dateL", 
                stock_livraison."codeL", stock_produit."nomP", 
                stock_lignelivraison."qte", stock_lignelivraison."prixHt",
                stock_lignelivraison.statut
                
                from stock_lignelivraison 
                left join stock_lignecommande on stock_lignelivraison.commande_id=stock_lignecommande.id
                left join stock_livraison on stock_lignelivraison.livraison_id=stock_livraison.id
                left join stock_produit on stock_lignelivraison.produit_id=stock_produit.id
                left join stock_commande on stock_commande.id = stock_lignecommande.commande_id
                where stock_lignelivraison.disponible=True
            """

    livraisons = LigneLivraison.objects.raw(query)
    return render(request, 'produitLivraison/produitlivraison.html', {"livraisons": livraisons})


@login_required(login_url="/login")
def create_listlivraison(request):
    titre = "Enregistrement"
    form = LigneLivraisonForm(request.POST or None)
    d = date.today().strftime("%d%m%Y")
    id_max = Livraison.objects.all().count()
    if (id_max == 0):
        id_max = 1
    else:
        id_max = id_max + 1
    ref_com = "LIV0" + str(d) + str(id_max)

    if request.method=='POST':
        date_L = request.POST['dateL']
        ref_L = request.POST['codeL']
        fournisseur = request.POST['fournisseur']
        cmd = request.POST.getlist('cmdIds[]')
        pdt = request.POST.getlist('pdtIds[]')
        qte = request.POST.getlist('qtePdt[]')
        prix = request.POST.getlist('prixPdt[]')
        if (pdt):
            liv = Livraison.objects.create(codeL=ref_L, dateL=date_L, fournisseur=fournisseur, auteurL=request.user)
            livraison_id = liv.id
            for i in range(len(pdt)):
                LigneLivraison.objects.create(livraison=Livraison.objects.get(pk=livraison_id), commande=LigneCommande.objects.get(pk=cmd[i]), produit=Produit.objects.get(pk=pdt[i]), qte=qte[i], prixHt=prix[i], auteurL=request.user)

            messages.success(request, "Enregistrement(s) effectué(s)")
            return redirect('livraisons')
        else:
            messages.warning(request, "Svp, Veuillez enregistrer au moins une ligne livraison de produit.")
            return render(request, 'produitLivraison/produitlivraison_form.html', {'form': form, 'codeL': ref_com, "titre": titre})

    return render(request, 'produitLivraison/produitlivraison_form.html', {'form': form, 'codeL': ref_com, "titre": titre})


def load_fourniture_cmd(request):
    cmd_ref = request.GET.get('lcmd_ref')
    f_cmd = Produit.objects.filter(lignecommande__id=cmd_ref).values('id', 'nomP')
    return render(request, 'produitLivraison/produit_cmd.html', {'f_cmd': f_cmd})


@login_required(login_url="/login")
def update_listlivraison(request, id):
    titre = "Modification"
    liv = get_object_or_404(LigneLivraison, id=id)
    form = LigneLivraisonForm(request.POST or None, instance=liv)
    # form = forms.fields['produit'].disabled = True

    if request.method=='POST':
        qte = request.POST['qte']
        prix = request.POST['prixHt']
        liv.qte = qte
        liv.prixHt = prix
        liv.save()
        messages.success(request, "Modification effectuée", extra_tags='custom-success')
        return redirect('livraisons')

    return render(request, 'produitLivraison/produitlivraison_forms.html', {'form': form, "titre": titre, "liv": liv})


@login_required(login_url="/login")
def delete_listlivraison(request, id):
    produitl = get_object_or_404(LigneLivraison, id=id)

    if produitl:
        produitl.disponible = False
        produitl.save()
        messages.success(request, "Suppression effectuée", extra_tags='custom-success')
        return redirect('/livraisons')

    return render(request, 'produitLivraison/produitlivraison.html', {'produitl': produitl})


@login_required(login_url="/login")
def validate_listlivraison(request, id):
    produitl = get_object_or_404(LigneLivraison, id=id)

    if produitl:
        produitl.statut = "VA"
        LigneCommande.objects.filter(id=produitl.commande_id).update(statut='LIVREE')
        current_datetime = timezone.now()
        Mouvement.objects.create(dateM=current_datetime.date(), llivraison=LigneLivraison.objects.get(pk=produitl.id),
                                 produit=Produit.objects.get(pk=produitl.produit_id), qte=produitl.qte, type='IN', auteurM=request.user)
        produitl.save()
        messages.success(request, "Livraison validée", extra_tags='custom-success')
        return redirect('/livraisons')
    else:
        messages.warning(request, "Une erreur est survenue", extra_tags='custom-warning')

    return render(request, 'produitLivraison/produitlivraison_forms.html', {'produitl': produitl})


@login_required(login_url="/login")
def tarifications(request):
    tarifications = Tarification.objects.filter(disponible=True).order_by('-id')
    return render(request, 'tarification/tarifications.html', {"tarifications": tarifications})


@login_required(login_url="/login")
def create_tarification(request):
    titre = "Enregistrement"
    if request.method == 'POST':
        form = TarificationForm(request.POST)
        if form.is_valid():
            tarification = form.save(commit=False)
            tarification.auteurT = request.user
            tarification.save()
            messages.success(request, "Enregistrement effectué", extra_tags='custom-success')
            return redirect("/create-tarification")
    else:
        form = TarificationForm()
    return render(request, 'tarification/tarification_form.html',  {"form": form, "titre": titre})


@login_required(login_url="/login")
def update_tarification(request, id):
    titre = "Modification"
    tarification = get_object_or_404(Tarification, id=id)
    form = TarificationForm(request.POST or None, instance=tarification)

    if form.is_valid():
        tarif = form.save(commit=False)
        if tarif.dateF is not None:
            tarif.vigeur = "OBSOLETE"
        tarif.save()
        messages.success(request, "Modification effectuée", extra_tags='custom-success')
        return redirect('/tarifications')

    return render(request, 'tarification/tarification_form.html', {'form': form, "titre": titre})


@login_required(login_url="/login")
def delete_tarification(request, id):
    tarification = get_object_or_404(Tarification, id=id)

    if tarification:
        tarification.disponible = False
        tarification.save()
        messages.success(request, "Suppression effectuée", extra_tags='custom-success')
        return redirect('/tarifications')

    return render(request, 'tarification/tarifications.html', {'tarification': tarification})


@login_required(login_url="/login")
def listVente(request):
    query = """
                select stock_lignevente.id, 
                stock_vente.client, stock_vente."dateV",
                stock_vente."codeV", stock_produit."nomP",
                stock_lignevente."qte", stock_tarification."prix",
                to_char(stock_lignevente."qte" * (cast(stock_tarification."prix" AS integer)), '9,999,999') as totalht,
                stock_lignevente.statut
                
                from stock_lignevente
                left join stock_vente on stock_lignevente.vente_id=stock_vente.id
                left join stock_produit on stock_lignevente.produit_id=stock_produit.id
                left join stock_tarification on stock_lignevente.tarification_id=stock_tarification.id
                where stock_lignevente.disponible=True
            """

    ventes = LigneVente.objects.raw(query)
    return render(request, 'produitVente/produitvente.html', {"ventes": ventes})


@login_required(login_url="/login")
def create_listventes(request):
    titre = "Enregistrement"
    form = LigneVenteForm(request.POST or None)
    d = date.today().strftime("%d%m%Y")
    id_max = Vente.objects.all().count()
    if (id_max == 0):
        id_max = 1
    else:
        id_max = id_max + 1
    ref_v = "VENT0" + str(d) + str(id_max)

    if request.method == 'POST':
        date_V = request.POST['dateV']
        ref_V = request.POST['codeV']
        client = request.POST['client']
        pdt = request.POST.getlist('pdtIds[]')
        prix = request.POST.getlist('prixIds[]')
        qte = request.POST.getlist('qte[]')
        if (pdt):
            ven = Vente.objects.create(codeV=ref_V, dateV=date_V, client=client, auteurV=request.user)
            vente_id = ven.id
            for i in range(len(pdt)):
                LigneVente.objects.create(vente=Vente.objects.get(pk=vente_id),
                                          produit=Produit.objects.get(pk=pdt[i]),
                                          qte=qte[i],
                                          tarification=Tarification.objects.get(pk=prix[i]),
                                          auteurL=request.user)

            messages.success(request, "Enregistrement(s) effectué(s)")
            return redirect('ventes')
        else:
            messages.warning(request, "Svp, Veuillez enregistrer au moins une ligne vente de produit.")
            return render(request, 'produitVente/produitvente_form.html',
                          {'form': form, 'codeV': ref_v, "titre": titre})

    return render(request, 'produitVente/produitvente_form.html',
                  {'form': form, 'codeV': ref_v, "titre": titre})


def load_tarif_produit(request):
    pdt_id = request.GET.get('pdt_id')
    p_tarif = Tarification.objects.filter(produit__id=pdt_id).values('id', 'prix')
    return render(request, 'produitVente/produit_tarif.html', {'p_tarif': p_tarif})


def load_qte_dispo(request):
    pdt_id = request.GET.get('pdt_id')

    qte_in = \
        list(Mouvement.objects.filter(produit_id=pdt_id, type='IN', disponible=True).aggregate(Sum('qte')).values())[
            0] or 0
    qte_out = \
    list(Mouvement.objects.filter(produit_id=pdt_id, type='OUT', disponible=True).aggregate(Sum('qte')).values())[
        0] or 0
    qte_dis = qte_in - qte_out

    return JsonResponse([qte_dis], safe=False)


@login_required(login_url="/login")
def delete_listvente(request, id):
    produitv = get_object_or_404(LigneVente, id=id)

    if produitv:
        produitv.disponible = False
        produitv.save()
        messages.success(request, "Suppression effectuée", extra_tags='custom-success')
        return redirect('/ventes')

    return render(request, 'produitVente/produitvente_forms.html', {'produitv': produitv})


@login_required(login_url="/login")
def validate_listvente(request, id):
    produitv = get_object_or_404(LigneVente, id=id)

    if produitv:
        produitv.statut = "VA"
        current_datetime = timezone.now()
        Mouvement.objects.create(dateM=current_datetime.date(), sortie=LigneVente.objects.get(pk=produitv.id),
                                 produit=Produit.objects.get(pk=produitv.produit_id), qte=produitv.qte, type='OUT', auteurM=request.user)
        produitv.save()
        messages.success(request, "Vente validée", extra_tags='custom-success')
        return redirect('/ventes')
    else:
        messages.warning(request, "Une erreur est survenue", extra_tags='custom-warning')

    return render(request, 'produitVente/produitvente.html', {'produitv': produitv})


@login_required(login_url="/login")
def situationStock(request):
    current_datetime = timezone.now()
    date_actuelle = current_datetime.date()
    date_debut = datetime(date_actuelle.year, date_actuelle.month, 1).date()
    date_mois = datetime(date_actuelle.year, date_actuelle.month, 1)
    query = """
                SELECT stock_produit.id AS id, stock_produit."nomP", stock_produit."codeP", stock_produit."mesureP", 
                stock_produit."quantiteMinP", stock_categorie."nomC",
                            sum(case
                                    when stock_mouvement."dateM" < %s
                                    then case stock_mouvement.type when 'OUT' then -1 else 1 end
                                    else 0
                                end * qte) AS st_init,
                            sum(case
                                    when stock_mouvement."dateM" BETWEEN %s AND %s
                                     AND stock_mouvement.type = 'IN' then qte
                                    else 0
                               end) AS qt_e,
                            sum(case
                                    when stock_mouvement."dateM" BETWEEN %s AND %s
                                     AND stock_mouvement.type = 'OUT' then qte
                                    else 0
                                end) AS qt_s,
                            sum(case stock_mouvement.type when 'OUT' then -1 else 1 end * qte) AS st_fin
                            FROM stock_produit
                            LEFT JOIN stock_mouvement on stock_produit.id=stock_mouvement.produit_id
                            INNER JOIN stock_categorie on stock_produit.categorie_id=stock_categorie.id
                            AND stock_mouvement.disponible = True
                            AND stock_mouvement."dateM" <= %s
                            GROUP BY stock_produit.id, stock_categorie."nomC"
                            ORDER BY stock_produit."nomP"
            """

    situations = Produit.objects.raw(query, [date_debut, date_debut, date_actuelle, date_debut, date_actuelle, date_actuelle])
    return render(request, 'situationStock/situations.html', {"situations": situations, "date_mois": date_mois})


@login_required(login_url="/login")
def etatstockvente(request):
    query = """
                select stock_lignevente.id, 
                stock_vente.client, stock_vente."dateV",
                stock_vente."codeV", stock_produit."nomP",
                stock_lignevente."qte", stock_tarification."prix",
                to_char(stock_lignevente."qte" * (cast(stock_tarification."prix" AS integer)), '9,999,999') as totalht,
                stock_lignevente.statut

                from stock_lignevente
                left join stock_vente on stock_lignevente.vente_id=stock_vente.id
                left join stock_produit on stock_lignevente.produit_id=stock_produit.id
                left join stock_tarification on stock_lignevente.tarification_id=stock_tarification.id
                where stock_lignevente.disponible=True
                and stock_vente."dateV" BETWEEN %s AND %s
            """

    if request.method == 'POST':
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        if date_debut <= date_fin:
            ventes = LigneVente.objects.raw(query, [date_debut, date_fin])
            return render(request, 'etat/ventes.html', {"ventes": ventes, "date_debut": date_debut, "date_fin": date_fin})
        else:
            messages.warning(request, "Veuillez choisir correctement les dates de début et fin", extra_tags='custom-warning')
    else:
        pass

    return render(request, 'etat/ventes.html', {"ventes": ""})\


@login_required(login_url="/login")
def etatstockproduitperiode(request):
    query = """
                SELECT stock_produit.id AS id, stock_produit."nomP", stock_produit."codeP", stock_produit."mesureP", 
                stock_produit."quantiteMinP", stock_categorie."nomC",
                            sum(case
                                    when stock_mouvement."dateM" < %s
                                    then case stock_mouvement.type when 'OUT' then -1 else 1 end
                                    else 0
                                end * qte) AS st_init,
                            sum(case
                                    when stock_mouvement."dateM" BETWEEN %s AND %s
                                     AND stock_mouvement.type = 'IN' then qte
                                    else 0
                               end) AS qt_e,
                            sum(case
                                    when stock_mouvement."dateM" BETWEEN %s AND %s
                                     AND stock_mouvement.type = 'OUT' then qte
                                    else 0
                                end) AS qt_s,
                            sum(case stock_mouvement.type when 'OUT' then -1 else 1 end * qte) AS st_fin
                            FROM stock_produit
                            LEFT JOIN stock_mouvement on stock_produit.id=stock_mouvement.produit_id
                            LEFT JOIN stock_categorie on stock_produit.categorie_id=stock_categorie.id
                            AND stock_mouvement.disponible = True
                            AND stock_mouvement."dateM" <= %s
                            GROUP BY stock_produit.id, stock_categorie."nomC"
                            ORDER BY stock_produit."nomP"
            """

    if request.method == 'POST':
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        if date_debut <= date_fin:
            situationp = Produit.objects.raw(query, [date_debut, date_debut, date_fin, date_debut, date_fin, date_fin])
            return render(request, 'etat/situation_periode.html', {"situationp": situationp, "date_debut": date_debut, "date_fin": date_fin})
        else:
            messages.warning(request, "Veuillez choisir correctement les dates de début et fin", extra_tags='custom-warning')
    else:
        pass

    return render(request, 'etat/situation_periode.html', {"situationp": ""})


class ViewPDF_Facture(View):
    def get(self, request, *args, **kwargs):
        if request.method == "GET" and 'id_vente' in request.GET:
            id_ligne_vente = request.GET.get('id_vente')
            query = """ 
                        SELECT stock_produit.id AS id, stock_vente."codeV", stock_produit."codeP", stock_produit."nomP", stock_lignevente.qte,
                        stock_tarification.prix, (stock_lignevente.qte * cast(stock_tarification."prix" AS integer)) AS totalht,
                        sum((stock_lignevente.qte * cast(stock_tarification."prix" AS integer)) * 1.18)
                        FROM stock_lignevente
                        LEFT JOIN stock_produit on stock_lignevente.produit_id=stock_produit.id
                        LEFT JOIN stock_vente on stock_lignevente.vente_id=stock_vente.id
                        LEFT JOIN stock_tarification on stock_lignevente.tarification_id=stock_tarification.id
                        WHERE stock_lignevente.disponible=True
                        AND stock_lignevente.id = %s
                        GROUP BY stock_produit.id, stock_vente."codeV",stock_lignevente.qte,stock_tarification.prix
                        ORDER BY stock_produit."nomP" ASC
                    """

            sit_v = LigneVente.objects.raw(query, [id_ligne_vente])
            data = {

                'fours': sit_v,
            }
            pdf = render_to_pdf('etat/facture/sit_periode.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            messages.warning(request, "Aucune donnée à exporter :-)")
            pass
