# Generated by Django 4.1.1 on 2023-09-04 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0011_lignevente_qtedispo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lignevente',
            name='qteDispo',
        ),
    ]