# Generated by Django 4.1.1 on 2023-09-03 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_alter_tarification_datef'),
    ]

    operations = [
        migrations.AddField(
            model_name='lignevente',
            name='qteDispo',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]