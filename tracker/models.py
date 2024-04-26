from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    bac = models.FloatField(null=True, blank=True)
    cigarette_toxins = models.FloatField(null=True, blank=True)
    alcohol_toxins = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.username


class AlcoholIntake(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ALCOHOL_TYPES = [
        ('BEER', 'Beer'),
        ('WINE', 'Wine'),
        ('LIQUOR', 'Liquor'),
        ('MIXED', 'Mixed Drink'),
    ]
    alcohol_type = models.CharField(max_length=6, choices=ALCOHOL_TYPES)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}  - {self.amount} drinks"


class CigaretteIntake(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    units = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}  - {self.units} cigarettes"
