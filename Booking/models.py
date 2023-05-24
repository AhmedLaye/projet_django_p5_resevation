from django.db import models

# Create your models here.
class voiture(models.Model):
    
    class transmission(models.TextChoices):
        Automatique = 'Automatique'
        Manuelle= 'Manuelle'

    marque = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=100)
    capacity = models.IntegerField()
    transmission = models.CharField(choices = transmission.choices,max_length=12)

    
