from django.db import models, connection
import csv
import json
from django.contrib.auth.models import User
import pandas as pd
from django.db import connection
import csv
#class du service vol
class Vol(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    depart_time = models.TimeField()
    depart_weekday = models.IntegerField()
    duration = models.DurationField()
    arrival_time = models.TimeField()
    arrival_weekday = models.IntegerField()
    flight_no = models.CharField(max_length=100)
    airline_code = models.CharField(max_length=100)
    airline = models.CharField(max_length=100)
    economy_fare = models.IntegerField(null=True)
    business_fare = models.IntegerField(null=True)
    first_fare = models.IntegerField(null=True)
    
class Reservationv(models.Model):
    email = models.EmailField()

    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.nom} {self.prenom} {self.email}"

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
    
    class boite(models.TextChoices):
        Automatique = 'Automatique'
        Manuelle= 'Manuelle'

    marque = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=100)
    capacity = models.IntegerField()
    transmission = models.CharField(choices = boite.choices,max_length=12)
    prix_location= models.IntegerField( default= 30000)
    image = models.CharField(max_length=100 , default='')

    
# with open('car_data.json') as file:
#     data = json.load(file)
    
# # Connexion à la base de données
# cnx = mysql.connector.connect(
#     host='localhost',
#     user='el_rawane',
#     password='007700',
#     database='gestion_reservation'
# )
 # Création d'un curseur pour exécuter des requêtes SQL
# cursor = cnx.cursor()
# for record in data:
#     print(record)
#     query = "INSERT INTO Booking_voiture (marque, model, fuel_type, capacity, transmission, prix_location, image) VALUES (%s, %s, %s, %s,%s , %s, %s)"
#     values = (record['marque'], record['model'], record['fuel_type'], record['capacity'], record['transmission'], record['prix_location'],record['image'])
#     cursor.execute(query, values)

# # Valider les modifications dans la base de données
# cnx.commit()

# # Fermer le curseur et la connexion
# cursor.close()
# cnx.close()

class Reservation_voiture(models.Model):
    voiture = models.ForeignKey(voiture,to_field='id' ,on_delete=models.CASCADE ,related_name='voiture_id')
    utilisateur = models.ForeignKey(User,to_field='id', on_delete=models.CASCADE , related_name='utilisateur_id')
    date_debut_location = models.DateField()
    date_fin_location = models.DateField()
    # Autres champs de la réservation
    