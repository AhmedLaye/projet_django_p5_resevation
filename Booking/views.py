from django.shortcuts import render, redirect, get_object_or_404
from amadeus import Client, ResponseError
import pandas as pd
import os
import csv
from Booking.models import Vol
from datetime import datetime, timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Reservation


def register(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1==password2:
            user = User.objects.create_user(email=email, username=nom,first_name=prenom,password=password1)
            user.save()
        # Rediriger vers la page de confirmation de réservation après l'inscription
        return redirect('index')

    return render(request, 'booking/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Booking/index.html')  # Redirige vers la page d'accueil après la connexion réussie
        else:
            # Gérer l'erreur d'authentification invalide
            error_message = "Identifiant ou mot de passe incorrect."
    else:
        error_message = ""
    
    return render(request, 'Booking/login.html', {'error_message': error_message})

def logout(request):
    logout(request)
    return redirect('Booking/index.html')  # Redirige vers la page d'accueil après la déconnexion



with open('vol.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        depart_time = datetime.strptime(row['depart_time'], '%H:%M:%S').time()
        arrival_time = datetime.strptime(row['arrival_time'], '%H:%M:%S').time()
        
        duration_str = row['duration']
        duration_parts = duration_str.split(':')
        duration = timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]), seconds=int(duration_parts[2]))
        
        vol = Vol(
            origin=row['origin'],
            destination=row['destination'],
            depart_time=depart_time,
            depart_weekday=int(row['depart_weekday']),
            duration=duration,
            arrival_time=arrival_time,
            arrival_weekday=int(row['arrival_weekday']),
            flight_no=row['flight_no'],
            airline_code=row['airline_code'],
            airline=row['airline'],
            economy_fare=int(row['economy_fare']) if row['economy_fare'] else None,
            business_fare=int(row['business_fare']) if row['business_fare'] else None,
            first_fare=int(row['first_fare']) if row['first_fare'] else None,
        )
        vol.save()

def reservation_vol_view(request):
    if request.method == 'POST':
        lieu_depart = request.POST.get('lieu_depart')
        lieu_destination = request.POST.get('lieu_destination')

        # Effectuez la recherche dans la base de données pour les vols correspondants
        vol = Vol.objects.filter(
            origin=lieu_depart,
            destination=lieu_destination,
        ).distinct()

        message =  lieu_depart + " pour " + lieu_destination
        context={'message':message,
                    'vols' : vol
                    }
        print(vol)
        return render(request, 'booking/reservation_vol.html', context)
    

    return render(request,  'booking/reservation_vol.html')

def confirmation_reserve(request, id):
     vol = get_object_or_404(Vol, pk=id)
     if request.method == 'POST':
        email = request.POST.get('email')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        # id_vol = request.POST.get('id_vol')

        # Vérifiez si l'email existe dans la base de données
        try:
            user = User.objects.get(email=email)
            # Email existe, affichez le message de réservation réussie
            message = "Réservation réussie"
        except User.DoesNotExist:
            # Email n'existe pas, redirigez vers la page de création de compte
            return redirect('register')

        # Enregistrez la réservation dans la base de données
        reservation = Reservation.objects.create(nom=nom, prenom=prenom,email=email)
        reservation.save()

        return render(request, 'booking/confirmation_reserve.html', {'message': message})

     return render(request, 'booking/confirmation_reserve.html',  {'vol':vol})

# from Booking.models import Hotels
# Create your views here.
def index_view(request):
    amadeus = Client(
        client_id='yMHEq6Q7ipGdqP8m6Fovtgn4xFwCAwNJ',
        client_secret='NBITauWAZGbzHNSN'
    )
    try:
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode='DKR')
        pd.DataFrame(response.data)      
        df = pd.DataFrame(response.data)
        df.to_csv(os.path.join(os.getcwd(), "hotels.csv"), index=False)
        print(response.data)

         # Get list of available offers in specific hotels by hotel ids
        hotels_by_city = amadeus.shopping.hotel_offers_search.get(cityCode='DKR',
        hotelIds='RTPAR001', adults='2', checkInDate='2023-10-01', checkOutDate='2023-10-04')       
        
        print(f"vous avez rechercher: {hotels_by_city.data}")
    except ResponseError as error:
        raise error
    

    return render(request,  'booking/index.html')

def voiture_view(request):

    return render(request,  'booking/voiture.html')

def vol_view(request):

    return render(request,  'booking/vol.html')

def resto_view(request):
    hotels = Hotels.objects.raw("SELECT * FROM  Booking_hotels")
    return render(request,  'booking/resto.html', {'hotels':hotels})