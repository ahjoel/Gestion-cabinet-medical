# Generated by Django 4.1.1 on 2023-09-01 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_categorie_disponiblec'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='mesureP',
            field=models.CharField(blank=True, choices=[('UNITE', 'UNITE'), ('CARTON 10', 'CARTON 10'), ('CARTON 20', 'CARTON 20')], default='', max_length=30),
        ),
    ]
