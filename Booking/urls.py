from django.urls import path

from .views  import *

urlpatterns =[
    path('', index_view, name='index'),
    path('voiture/', voiture_view, name='voiture')
    
]