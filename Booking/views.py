from django.shortcuts import render

# Create your views here.
def index_view(request):

    return render(request,  'booking/index.html')

def voiture_view(request):

    return render(request,  'booking/voiture.html')

def vol_view(request):

    return render(request,  'booking/vol.html')

def resto_view(request):

    return render(request,  'booking/resto.html')