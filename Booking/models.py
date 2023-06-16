from django.db import models
import csv
from django.db import models
import pandas as pd
from django.db import connection
import csv
import json
import  amadeus
# Create your models here.
class Utilisateur(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=100)
    # Autres champs utilisateur
    numero_telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=100)


class Hotels(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    description = models.TextField()
    note = models.CharField(max_length=100)
    # Autres champs sur l'hôtel
    site_web = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    
    @staticmethod
    def import_data_from_csv():
        with open('hotels.csv', 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)  # Skip the header row
            with connection.cursor() as cursor:
                for row in csv_data:
                    nom = row[3]
                    adresse = row[1]
                    description = row[2]
                    note = row[3]
                    site_web = row[4]
                    telephone = row[0]

                    # Vérifier l'existence des données avant de les insérer
                    query_check = "SELECT * FROM Booking_hotels WHERE nom = %s"
                    cursor.execute(query_check, [nom])
                    result = cursor.fetchone()
                    if not result:
                        query_insert = """
                            INSERT INTO Booking_hotels (nom, adresse, description, note, site_web, telephone)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query_insert, [nom, adresse, description, note, site_web, telephone])

Hotels.import_data_from_csv()

class Chambre(models.Model):
    hotel = models.CharField(max_length=50)
    type_chambre = models.CharField(max_length=50)
    description = models.TextField()
    prix_nuit = models.DecimalField(max_digits=8, decimal_places=2)
    offre_id = models.CharField(max_length=50)

    @staticmethod
    def insert_chambres_from_csv():
        with open('rooms.csv', 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)  # Skip the header row

            for row in csv_data:
                # Extraction des données du fichier CSV
                hotel_data = json.loads(row[1].replace("'", '"'))
                hotel = hotel_data['hotelId']
                type_chambre = row[0]
                offre_data = json.loads(row[3].replace("'", '"'))
                offre_id = offre_data[0]['id']
                description = offre_data[0]['room']['description']['text']
                prix_nuit = offre_data[0]['price']['base']

                # Construction de la requête SQL d'insertion
                query_insert = """
                    INSERT INTO Booking_chambre (hotel, type_chambre, description, prix_nuit, offre_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
                # Exécution de la requête SQL avec les valeurs correspondantes
                with connection.cursor() as cursor:
                    cursor.execute("DELETE  FROM Booking_chambre")
                    cursor.execute(query_insert, [hotel, type_chambre, description, prix_nuit,offre_id])
Chambre.insert_chambres_from_csv()
    


class Reservation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    date_arrivee = models.DateField()
    date_depart = models.DateField()
    # Autres champs de la réservation
    nombre_invite = models.IntegerField()

# Create your model
class voiture(models.Model):
    
    class transmission(models.TextChoices):
        Automatique = 'Automatique'
        Manuelle= 'Manuelle'

    marque = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=100)
    capacity = models.IntegerField()
    transmission = models.CharField(choices = transmission.choices,max_length=12)

    
