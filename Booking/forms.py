 
from django import forms

class ReservationForm(forms.Form):
    # name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control  my-0flex d-', 'type':'hidden','value':'testing'}))
    # email = forms.EmailField(label="Email", max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control','type':'hidden','value':'testing'}))
    date_arrive = forms.DateField(label="Check-in date", widget=forms.DateInput(attrs={'class': 'form-control date', 'type': 'date'}))
    date_depart = forms.DateField(label="Check-out date", widget=forms.DateInput(attrs={'class': 'form-control date', 'type': 'date'}))
    number_of_guests = forms.IntegerField(label="Number of guests", widget=forms.NumberInput(attrs={'class': 'form-control ', 'type':'number'}))
    room_type = forms.ChoiceField(label="Room type", choices=[("single", "Single"), ("double", "Double"), ("suite", "Suite")], widget=forms.Select(attrs={'class': 'form-control wide'}))
    payment_method = forms.ChoiceField(label="Payment method", choices=[("Orange Money", "Orange Money"), ("wave", "Wave"), ("paypal", "Paypal"), ("other", "Other")], widget=forms.Select(attrs={'class': 'form-control form-floating'}))
