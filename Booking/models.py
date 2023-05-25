from django.db import models, connection
import csv
import json




from django.db import models
import pandas as pd
from django.db import connection
import csv
#class du service vol
class Client(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
# Autres champs utilisateur
numero_telephone = models.CharField(max_length=20)
adresse = models.CharField(max_length=100)

class Passager(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
class Vol(models.Model):
    dateDepart = models.DateField(max_length=50)
    heureDepart = models.DateTimeField(max_length=50)
    dateArrivee = models.DateField(max_length=50)
    heureArrivee = models.DateTimeField(max_length=50)
class Reserve(models.Model):
    date = models.DateTimeField(max_length=50)
    numero = models.CharField(max_length=50)
class Compagnie(models.Model):
    nom = models.CharField(max_length=50)
class Ville(models.Model):
    nom = models.CharField(max_length=50)
class Aeroport(models.Model):
    nom = models.CharField(max_length=50)
#class du service vol
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
    note_moyenne = models.CharField(max_length=100)
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
                    note_moyenne = row[3]
                    site_web = row[4]
                    telephone = row[0]

                    # Vérifier l'existence des données avant de les insérer
                    query_check = "SELECT * FROM Booking_hotels WHERE nom = %s"
                    cursor.execute(query_check, [nom])
                    result = cursor.fetchone()
                    if not result:
                        query_insert = """
                            INSERT INTO Booking_hotels (nom, adresse, description, note_moyenne, site_web, telephone)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query_insert, [nom, adresse, description, note_moyenne, site_web, telephone])

Hotels.import_data_from_csv()

class Chambre(models.Model):
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE)
    type_chambre = models.CharField(max_length=50)
    description = models.TextField()
    prix_nuit = models.DecimalField(max_digits=8, decimal_places=2)
    disponibilite = models.BooleanField(default=True)


class Reservation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    date_arrivee = models.DateField()
    date_depart = models.DateField()
    # Autres champs de la réservation
    nombre_invite = models.IntegerField()

# Create your models here.
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

    
with open('car_data.json') as file:
    data = json.load(file)
    
# Connexion à la base de données
with connection.cursor() as cursor:
# Création d'un curseur pour exécuter des requêtes SQL
    
    for record in data:
        query = "INSERT INTO Booking_voiture (marque, model, year, fuel_type, capacity, transmission) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (record['marque'], record['model'], record['year'], record['fuel_type'], record['capacity'], record['transmission'])
        cursor.execute(query, values)

   
