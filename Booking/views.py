from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from amadeus import Client, ResponseError
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
import pandas as pd
import os
from Booking.models import Hotels,Chambre, Reservation
from datetime import datetime,timedelta



# Create your views here.
amadeus = Client(
        client_id='yMHEq6Q7ipGdqP8m6Fovtgn4xFwCAwNJ',
        client_secret='NBITauWAZGbzHNSN'
    )

def index_view(request):
    
    return render(request,  'booking/index.html')

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
    # if request.method== 'POST':
    #     reservation =Reservation(utilisateur="1", chambre=chambre, date_arrivee=datetime.now(), date_depart=datetime.now(),
    #                                   nombre_invite=1)
    #     reservation.save()
    #     message='reussi'
        
        # return render(request, 'booking/reservation/chambre.html', {'chambre':chambre, 'message':message})

    return render(request, 'booking/reservation/chambre.html', {'chambre':chambre})
    



