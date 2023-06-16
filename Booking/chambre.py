import csv
import random
import pandas as pd


DESCRIPTIONS = [
    "Belle chambre avec vue sur la mer",
    "Chambre confortable avec balcon",
    "Suite spacieuse avec jacuzzi",
    "Chambre moderne avec télévision à écran plat",
    "Chambre élégante avec décoration raffinée",
    # Ajoutez d'autres descriptions ici
]

data = []

with open('../hotels.csv', 'r') as file:
    hotels_data = csv.reader(file)
    next(hotels_data)
    for row in hotels_data:  # Skip the header row                                                               
        # ici je fixe 10 chambre pour chaque hotel
        for i in range(10):
            chambre = {
                "nom": "Chambre {}".format(i),
                "description": random.choice(DESCRIPTIONS),
                "prix": random.randint(25000, 40000),
                "etage":random.randint(1,20),   
                "id_hotel": row[4],
                "checkInDate":'',
                "checkOutDate":'',
                "roomQuantity": ''
                # Ajouter d'autres champs de modèle et attribuer des valeurs aléatoires en conséquence
            }
            data.append(chambre)
# Enregistrer les données dans un fichier CSV
filename = "chambres_data.csv"

with open(filename, "w", newline="") as csvfile:
    fieldnames = [key for key, value in chambre.items()]  # Modifier les noms des champs selon votre modèle
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data)

print("Fichier CSV créé avec succès :", filename)
