from django.shortcuts import render
from amadeus import Client, ResponseError
import pandas as pd
import os
from Booking.models import Hotels
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