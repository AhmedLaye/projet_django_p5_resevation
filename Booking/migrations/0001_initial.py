# Generated by Django 4.2.1 on 2023-06-17 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chambre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hotel", models.CharField(max_length=50)),
                ("type_chambre", models.CharField(max_length=50)),
                ("description", models.TextField()),
                ("prix_nuit", models.DecimalField(decimal_places=2, max_digits=8)),
                ("offre_id", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Hotels",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
                ("adresse", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("note", models.CharField(max_length=100)),
                ("site_web", models.CharField(max_length=100)),
                ("telephone", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Utilisateur",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=50)),
                ("prenom", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("mot_de_passe", models.CharField(max_length=100)),
                ("numero_telephone", models.CharField(max_length=20)),
                ("adresse", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="voiture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("marque", models.CharField(max_length=100)),
                ("model", models.CharField(max_length=100)),
                ("fuel_type", models.CharField(max_length=100)),
                ("capacity", models.IntegerField()),
                (
                    "transmission",
                    models.CharField(
                        choices=[
                            ("Automatique", "Automatique"),
                            ("Manuelle", "Manuelle"),
                        ],
                        max_length=12,
                    ),
                ),
                ("prix_location", models.IntegerField(default=30000)),
                ("image", models.CharField(default="", max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Reservation_voiture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_debut_location", models.DateField()),
                ("date_fin_location", models.DateField()),
                (
                    "utilisateur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="utilisateur_id",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "voiture",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="voiture_id",
                        to="Booking.voiture",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_arrivee", models.DateField()),
                ("date_depart", models.DateField()),
                ("nombre_invite", models.IntegerField()),
                (
                    "chambre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Booking.chambre",
                    ),
                ),
                (
                    "utilisateur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
