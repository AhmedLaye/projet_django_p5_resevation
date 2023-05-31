from django.shortcuts import render , get_object_or_404 ,redirect
from amadeus import Client, ResponseError
import pandas as pd
import os
from Booking.models import Hotels
from Booking.models import voiture
from Booking.models import Reservation_voiture
from Booking.forms import ReservCarForm
from Booking.models import Utilisateur
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


def car_reservation(request ,car_id):
    
    car = get_object_or_404( voiture, id = car_id)
    
    if request.method == 'POST':

        date_debut = request.POST['date_debut']  # Date de début de réservation
        date_fin = request.POST['date_fin']  # Date de fin de réservation

    
        # Création de l'objet réservation
        reservation = Reservation_voiture( id_voiture =car_id, date_debut=date_debut, date_fin=date_fin)
        reservation.save()
        
        return redirect('page_de_confirmation')  # Rediriger vers une page de confirmation

    return render(request, 'booking/voiture.html')

    