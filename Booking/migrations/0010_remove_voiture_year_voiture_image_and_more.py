# Generated by Django 4.2.1 on 2023-06-12 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Booking", "0009_remove_voiture_year_voiture_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="voiture",
            name="year",
        ),
        migrations.AddField(
            model_name="voiture",
            name="image",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AddField(
            model_name="voiture",
            name="prix_location",
            field=models.IntegerField(default=30000),
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
                        to="Booking.utilisateur",
                    ),
                ),
                (
                    "voiture",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Booking.voiture",
                    ),
                ),
            ],
        ),
    ]