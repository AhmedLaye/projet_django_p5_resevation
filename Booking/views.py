from django.shortcuts import render , get_object_or_404 ,redirect
from amadeus import Client, ResponseError
import pandas as pd
import os
from Booking.models import Hotels
from Booking.models import voiture
from Booking.models import Reservation_voiture
from Booking.forms import ReservCarForm
from Booking.models import Utilisateur
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    voitures=voiture.objects.raw("SELECT * FROM Booking_voiture WHERE id IN (1,2,3,4,5,6)")

    return render(request,  'booking/voiture.html',{'voitures':voitures})

def vol_view(request):

    return render(request,  'booking/vol.html')

def resto_view(request):
    hotels = Hotels.objects.raw("SELECT * FROM  Booking_hotels")
    return render(request,  'booking/resto.html', {'hotels':hotels})

def detail_voiture_view(request ,car_id):
    car = get_object_or_404( voiture, id = car_id)

    return render(request,  'booking/detail_voiture.html' , {'car':car})

@login_required (login_url='connection')
def car_reservation(request):
    
    
    if request.method == 'POST':
        
        date_debut = request.POST['date_debut']  # Date de début de réservation
        date_fin = request.POST['date_fin']# Date de fin de réservation
        voiture_id = request.POST['identifiant_voiture']
        utilisateur_id=request.user.id
    
        # Création de l'objet réservation
        reservation = Reservation_voiture( utilisateur_id=utilisateur_id ,voiture_id=voiture_id,date_debut_location=date_debut, date_fin_location=date_fin)
        reservation.save()
        
        return redirect('voiture')  # Rediriger vers une page de confirmation

    return render(request, 'voiture')

def register(request):
    if request.method =='POST':
        nom_utilisateur=request.POST['name']
        email=request.POST['email']
        password=request.POST['pass']
        password1=request.POST['re_pass']
       
        if password != password1:
            message_erreur='les mots de pass ne sont pas conformes'
            return render(request, 'booking/register.html', {'message_erreur': message_erreur})
            
        user= User.objects.create_user(nom_utilisateur,email,password)

        user.save()
    
    return render(request, 'booking/register.html')


def connection(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, 'Connexion réussie ')
            return redirect('voiture')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
     
    return render(request, 'booking/connection.html')

def deconnection(request):
    logout(request)
    return redirect('voiture')

    
    