# Generated by Django 4.2.1 on 2023-06-17 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Booking", "0005_remove_chambre_genre_chambre_offre_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="utilisateur",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
