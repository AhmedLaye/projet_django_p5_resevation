from django.urls import path

from .views  import *
from Booking import views

urlpatterns =[
    path('', index_view, name='index'),
    path('voiture/', voiture_view, name='voiture'),
    path('vol/', vol_view, name='vol'),
    path('resto/', resto_view, name='resto'),
    path('voiture/<int:car_id>/', detail_voiture_view, name='details') ,
    path('reservation/', views.car_reservation, name='reservation'),
    path('inscription/', views.inscription, name='inscription'),
    path('connection/', views.connection, name='connection'),
    path('deconnection/', views.deconnection, name='deconnection'),
    path('reservation_vol/', reservation_vol_view,name='reservation'),
    path('reservation/<int:id>/', confirmation_reserve, name='confirmation_reserve'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout')

]