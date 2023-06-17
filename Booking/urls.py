from django.urls import path

from .views import *

urlpatterns =[
    path('', index_view, name='index'),
    path('resto/', resto_view, name='resto'),
    path('detail/<int:id>/', hotel_detail, name='hotel_view'),
    path('reserver_hotel/<int:id>/', reserver_hotel, name='reserver_hotel'),
    # path('login/', login_view, name='login'),
    path('reserver_chambre/<int:id>/', reserver_chambre, name='reserver_chambre'),
    
]