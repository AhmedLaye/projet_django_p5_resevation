from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from amadeus import Client, ResponseError
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
import pandas as pd
import os
from Booking.models import Hotels,Chambre
from datetime import datetime,timedelta



# Create your views here.
amadeus = Client(
        client_id='yMHEq6Q7ipGdqP8m6Fovtgn4xFwCAwNJ',
        client_secret='NBITauWAZGbzHNSN'
    )
try:
    response = amadeus.reference_data.locations.hotels.by_city.get(cityCode='MAD')
    
    
    
    pd.DataFrame(response.data)      
    df = pd.DataFrame(response.data)
    df.to_csv(os.path.join(os.getcwd(), "hotels.csv"), index=False)

except ResponseError as error:
    raise error
def index_view(request):
    try:
        all_id=[hotel.get('hotelId') for hotel in response.data[:100]]
        # check_in_date = check_in_date = (pd.to_datetime('today') + pd.DateOffset(days=1)).strftime('%Y-%m-%d')
        # check_out_date = (pd.to_datetime('today') + pd.DateOffset(days=2)).strftime('%Y-%m-%d')
        search_hotels = amadeus.shopping.hotel_offers_search.get(hotelIds=all_id)
        
        print("**************************")
        print(search_hotels.data[0])
        print("µµµµµµµµµµµµµµµµµµµµµµµµµµµ")
        

    except ResponseError as error:
        raise error
    
    return render(request,  'booking/index.html')

def voiture_view(request):

    return render(request,  'booking/voiture.html')

def vol_view(request):


    return render(request,  'booking/vol.html')

def resto_view(request):
    hotels = Hotels.objects.raw("SELECT * FROM  Booking_hotels")
    
    return render(request,  'booking/resto.html',{'hotels':hotels,} )

def hotel_detail(request, id):
    
    hotel = Hotels.objects.get(id=id)
    
    return render(request, 'booking/hotel_detail.html', {'hotel': hotel})


def reserver_hotel(request, id):
    hotel = Hotels.objects.get(id=id)
    
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ReservationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            date_arrive = form.cleaned_data['date_arrive']
            date_depart = form.cleaned_data['date_depart']
            try:
            # Get list of available offers in specific hotels by hotel ids
                hotels_by_city = amadeus.shopping.hotel_offers_search.get(
                    hotelIds=hotel.site_web, checkInDate=date_arrive, checkOutDate=date_depart)
                message = ""
                message_error=""
                room_price=""
                room_descript=""
                chambre=""
                
                data=hotels_by_city.data
                
                if len(data)!=0:
                    offerId = data[0]['offers'][0]['id']
                    guests = [{'id': 1, 'name': {'title': 'MR', 'firstName': 'BOB', 'lastName': 'SMITH'},
                        'contact': {'phone': '+33679278416', 'email': 'bob.smith@email.com'}}]
                    payments = {'id': 1, 'method': 'creditCard', 'card': {
                        'vendorCode': 'VI', 'cardNumber': '4151289722471370', 'expiryDate': '2027-08'}}

        # Hotel booking API to book the offer 
                    hotel_booking = amadeus.booking.hotel_bookings.post(
                    offerId, guests, payments)
                    print("******************************************")
                    print(hotel_booking.data)
                    print("******************************************")
                        # 2023-10-01'
                    print(data)
                    room_price = data[0]['offers'][0]['price']['base']
                    room_descript= data[0]['offers'][0]['room']['description']['text']
                    pd.DataFrame(data).to_csv(os.path.join(os.getcwd(), "rooms.csv"), index=False)
                    chambre=Chambre.objects.all()
                    print(hotel.site_web)
                    message="Des chambres sont disponibles"
                        
                else:
                    message_error="pas de chambre disponible"
            except ResponseError as error:
                message_error="hotel indisponible "
                return render(request,"booking/hotel_detail.html",
    {"form": form, "hotel":hotel,'message_error':message_error,})  

            
            return render(request, 'booking/hotel_detail.html',
            {'hotel':hotel, 'message':message,'message_error':message_error, 
            'date_arrive': date_arrive, 'date_depart': date_depart,
            'room_price':room_price,'room_descript':room_descript,'data':data, 'chambre':chambre
            })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReservationForm()

    return render(request,"booking/reservation/hotel.html",
    {"form": form, "hotel":hotel,})

def reserver_chambre(request, id):
    chambre=Chambre.objects.get(id=id)

    
    return render(request, 'booking/reservation/chambre.html', {'chambre':chambre})
    



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                
                request.session['username'] = username
                if 'username' in request.session:
                    username = request.session['username']
                    # L'utilisateur est connecté, vous pouvez effectuer les actions souhaitées ici
                    return render(request, 'booking/index.html', {'username': username}) # Remplacez '/dashboard/' par l'URL souhaitée en cas d'authentification réussie
            else:
                
                error_message = "Mot de passe incorrect."
                return render(request, 'booking/connexion/login.html', {'error_message': error_message})
        except User.DoesNotExist:
            # Nom d'utilisateur invalide, afficher un message d'erreur
            error_message = "Nom d'utilisateur invalide."
            return render(request, 'booking/connexion/login.html', {'error_message': error_message})

       
        return HttpResponse("connexion reussi pour l'instant")  # Remplacez '/dashboard/' par l'URL souhaitée

    return render(request, 'booking/connexion/login.html')