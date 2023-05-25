from django.shortcuts import render
from amadeus import Client, ResponseError
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
import pandas as pd
import os
from Booking.models import Hotels
# Create your views here.
amadeus = Client(
        client_id='yMHEq6Q7ipGdqP8m6Fovtgn4xFwCAwNJ',
        client_secret='NBITauWAZGbzHNSN'
    )
def index_view(request):
   
    try:
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode='DKR')
        pd.DataFrame(response.data)      
        df = pd.DataFrame(response.data)
        df.to_csv(os.path.join(os.getcwd(), "hotels.csv"), index=False)
    
        print(response.data)
        # recuperartion des id des hotels
        hotelIds = [hotel.get('hotelId') for hotel in response.data]
     
        
        print(f'liste des id : {hotelIds}')
        print("*****************************************")
        print(hotel_offers.data)
    except ResponseError as error:
        raise error
    

    

    return render(request,  'booking/index.html')

def voiture_view(request):

    return render(request,  'booking/voiture.html')

def vol_view(request):

    return render(request,  'booking/vol.html')

def resto_view(request):
    hotels = Hotels.objects.raw("SELECT * FROM  Booking_hotels")
    
   
        

    return render(request,  'booking/resto.html', {'hotels':hotels,})

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
                # Hotel List API to get list of Hotels by city code
                # Hotel Search API to get list of offers for a specific hotel
                hotel_offers = amadeus.shopping.hotel_offers_search.get(
                    hotelIds=hotel.site_web, adults='2  ', checkInDate=date_arrive, checkOutDate=date_depart)
                print(f" liste des offres disponible: {hotel_offers.data}")
                print(hotel_offers.length)

                

                
                # offerId = hotel_offers.data[0]['offers'][0]['id']

                # guests = [{'id': 1, 'name': {'title': 'MR', 'firstName': 'BOB', 'lastName': 'SMITH'},
                #         'contact': {'phone': '+33679278416', 'email': 'bob.smith@email.com'}}]
                # payments = {'id': 1, 'method': 'creditCard', 'card': {
                #     'vendorCode': 'VI', 'cardNumber': '4151289722471370', 'expiryDate': '2027-08'}}
                    
                # hotel_booking = amadeus.booking.hotel_bookings.post(
                #     offerId, guests, payments)
                # print(hotel_booking.data)
               
               
            except ResponseError as error:
                raise error
                # Hotel booking API to book the offer 
                
           
            return render(request, 'booking/hotel_detail.html',{'hotel':hotel, 'message':message, 'date_arrive': date_arrive, 'date_depart': date_depart})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReservationForm()

    return render(request,"booking/reservation/hotel.html",{"form": form, "hotel":hotel,})
