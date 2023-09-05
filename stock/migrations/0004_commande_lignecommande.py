# Generated by Django 4.1.1 on 2023-09-01 23:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0003_produit_mesurep'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeC', models.CharField(max_length=10, unique=True)),
                ('dateC', models.DateField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('auteurC', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(choices=[('EN COURS', 'EN COURS'), ('LIVREE', 'LIVREE')], default='EN COURS', max_length=15)),
                ('qte', models.IntegerField()),
                ('disponible', models.BooleanField(default=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('auteurC', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stock.commande')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stock.produit')),
            ],
        ),
    ]