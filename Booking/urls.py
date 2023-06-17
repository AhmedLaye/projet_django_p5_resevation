from django.urls import path

<<<<<<< HEAD
from .views import *

urlpatterns =[
    path('', index_view, name='index'),
    path('resto/', resto_view, name='resto'),
    path('detail/<int:id>/', hotel_detail, name='hotel_view'),
    path('reserver_hotel/<int:id>/', reserver_hotel, name='reserver_hotel'),
    # path('login/', login_view, name='login'),
    path('reserver_chambre/<int:id>/', reserver_chambre, name='reserver_chambre'),
=======
from .views  import *
from Booking import views

urlpatterns =[
    path('', index_view, name='index'),
    path('voiture/', voiture_view, name='voiture'),
    path('vol/', vol_view, name='vol'),
    path('resto/', resto_view, name='resto'),
    path('voiture/<int:car_id>/', detail_voiture_view, name='details') ,
    path('reservation/', views.car_reservation, name='reservation'),
    path('register/', views.register, name='register'),
    path('connection/', views.connection, name='connection'),
    path('deconnection/', views.deconnection, name='deconnection')

>>>>>>> origin/master
    
]