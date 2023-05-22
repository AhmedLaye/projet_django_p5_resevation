from django.urls import path

from .views  import *

urlpatterns =[
    path('', index_view, name='index'),
    path('voiture/', voiture_view, name='voiture'),
    path('vol/', vol_view, name='vol'),
    path('resto/', resto_view, name='resto')
    
]