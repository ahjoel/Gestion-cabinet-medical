from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='/'),
    path('sign-up', views.sign_up, name='sign-up'),

    path('categories', views.categories, name='categories'),
    path('create-categorie', views.create_category, name='create-categorie'),
    path('update-categorie/<int:id>', views.update_category, name='update-categorie'),
    path('delete-categorie/<int:id>', views.delete_category, name='delete-categorie'),

    path('produits', views.produits, name='produits'),
    path('create-produit', views.create_produit, name='create-produit'),
    path('update-produit/<int:id>', views.update_produit, name='update-produit'),
    path('delete-produit/<int:id>', views.delete_produit, name='delete-produit'),

    path('commandeconsuls', views.commandeconsuls, name='commandeconsuls'),
    path('create-commandeconsul', views.create_commandeconsul, name='create-commandeconsul'),
    path('update-commandeconsul/<int:id>', views.update_commandeconsul, name='update-commandeconsul'),
    path('delete-commandeconsul/<int:id>', views.delete_commandeconsul, name='delete-commandeconsul'),

    path('lcommandes', views.listCommande, name='lcommandes'),
    path('create-lcommandes', views.create_listcommande, name='create-lcommandes'),
    path('update-produitcommande/<int:id>', views.update_lignecommande, name='update-produitcommande'),
    path('delete-produitcommande/<int:id>', views.delete_lignecommande, name='delete-produitcommande'),

    path('livraisons', views.listLivraison, name='livraisons'),
    path('create-llivraisons', views.create_listlivraison, name='create-llivraisons'),
    path('update-llivraisons/<int:id>', views.update_listlivraison, name='update-llivraisons'),
    path('delete-llivraisons/<int:id>', views.delete_listlivraison, name='delete-llivraisons'),
    path('validate-llivraisons/<int:id>', views.validate_listlivraison, name='validate-llivraisons'),
    path('ajax/load_cmd/', views.load_fourniture_cmd, name='ajax_load_fcmd'),

    path('tarifications', views.tarifications, name='tarifications'),
    path('create-tarification', views.create_tarification, name='create-tarification'),
    path('update-tarification/<int:id>', views.update_tarification, name='update-tarification'),
    path('delete-tarification/<int:id>', views.delete_tarification, name='delete-tarification'),

    path('ventes', views.listVente, name='ventes'),
    path('create-vente', views.create_listventes, name='create-vente'),
    path('ajax_load_tarif/', views.load_tarif_produit, name='ajax_load_tarif'),
    path('ajax_load_qte/', views.load_qte_dispo, name='ajax_load_qte'),
    path('delete-vente/<int:id>', views.delete_listvente, name='delete-vente'),
    path('validate-vente/<int:id>', views.validate_listvente, name='validate-vente'),
    path('pdf_view/', views.ViewPDF_Facture.as_view(), name='pdf_view'),

    path('situations', views.situationStock, name='situations'),
    path('etat_vente', views.etatstockvente, name='etat_vente'),
    path('etat_situationstock', views.etatstockproduitperiode, name='etat_situationstock'),
]
