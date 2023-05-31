from django.urls import path

from .views  import *
from Booking import views

urlpatterns =[
    path('', index_view, name='index'),
    path('voiture/', voiture_view, name='voiture'),
    path('vol/', vol_view, name='vol'),
    path('resto/', resto_view, name='resto'),
    path('voiture/<int:car_id>/', detail_voiture_view, name='details') ,
    path('reservation/<int:car_id>/', views.car_reservation, name='reservation')

    
]