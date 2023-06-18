from django import forms



Moyen_payement=(
    ("OM","Orange Money"),
    ("wave","Wave"),
    ("Pay Pal","Pay Pal")
)

class ReservCarForm(forms.Form):
    date_debut=forms.DateTimeField()
    date_fin=forms.DateTimeField()
    Mode_payement=forms.ChoiceField(choices=Moyen_payement)