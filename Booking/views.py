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
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode='PAR')
        pd.DataFrame(response.data)      
        df = pd.DataFrame(response.data)
        df.to_csv(os.path.join(os.getcwd(), "hotels.csv"), index=False)
    
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
            
            message="succes"
                
           
            return render(request, 'booking/hotel_detail.html',{'hotel':hotel, 'message':message, 'date_arrive': date_arrive, 'date_depart': date_depart})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReservationForm()

    return render(request,"booking/reservation/hotel.html",{"form": form, "hotel":hotel,})
