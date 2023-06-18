from django.shortcuts import render,redirect
from django.shortcuts import render , get_object_or_404 ,redirect
from amadeus import Client, ResponseError
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
import pandas as pd
import os
from Booking.models import Hotels,Chambre, Reservation,Reservation_voiture, voiture, Utilisateur
from datetime import datetime,timedelta
from Booking.forms import ReservCarForm, ReservationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings



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
    if request.method== 'POST':
        reservation =Reservation(utilisateur=request.user, chambre=chambre, date_arrivee=datetime.now(), date_depart=datetime.now(),
                                      nombre_invite=1)
        reservation.save()
        message='Reservation réussie'
        user=request.user
        subject = 'Confirmation de réservation'
        context = {'user': user, 'chambre': chambre}
        html_content = render_to_string('booking/email/email.html', context)
        email = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [user.email])
        email.content_subtype = 'html'
        email.send()
            
        
        return render(request, 'booking/reservation/chambre.html', {'chambre':chambre, 'message':message})

    return render(request, 'booking/reservation/chambre.html', {'chambre':chambre})
    
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
            return redirect('index')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
     
    return render(request, 'booking/connection.html')

def deconnection(request):
    logout(request)
    return redirect('voiture')

    
def recherches_voitures(request):
    if request.method == 'POST':
        date_debut = request.POST['date_debut']
        date_fin = request.POST['date_fin']

        # Requête pour récupérer les voitures disponibles
        voitures_disponibles = voiture.objects.exclude(
            reservation__date_debut_reservation__lte=date_fin,
            reservation__date_fin_reservation__gte=date_debut
        )

        context = {
            'voitures_disponibles': voitures_disponibles,
            'date_debut': date_debut,
            'date_fin': date_fin
        }

        return render(request, 'results.html', context)

    return render(request, 'search.html')
