from django.urls import path

from .views  import *

urlpatterns =[
    path('', index_view, name='index'),
    path('voiture/', voiture_view, name='voiture'),
    path('vol/', vol_view, name='vol'),
    path('resto/', resto_view, name='resto'),
    path('detail/<int:id>/', hotel_detail, name='hotel_view'),
    path('reserver_hotel/<int:id>/', reserver_hotel, name='reserver_hotel'),
    
]