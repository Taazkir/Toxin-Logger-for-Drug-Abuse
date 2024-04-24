from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def calculate_alcohol_toxins(self):
        # cigarettes = DrugIntake.objects.filter(user=self, drug_type='cigarette').count()

        alcohol_toxins = {
            'beer': 0.05,
            'wine': 0.12,
            'liquor': 0.4,
            'mixed_drink': 0.2,
        }

        total_alcohol_toxins = sum(
            [alcohol_toxins[alcohol.alcohol_type.lower()] * alcohol.amount for alcohol in self.alcoholintake_set.all()])

    def __str__(self):
        return self.username


# class DrugIntake(models.Model):
#     DRUG_CHOICES = (
#         ('cigarette', 'Cigarette'),
#         ('alcohol', 'Alcohol'),
#     )
#
#     ALCOHOL_TYPE_CHOICES = (
#         ('beer', 'Beer'),
#         ('wine', 'Wine'),
#         ('liquor', 'Liquor'),
#         ('mixed_drink', 'Mixed Drink'),
#     )
#
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     drug_type = models.CharField(max_length=50, choices=DRUG_CHOICES)
#     alcohol_type = models.CharField(max_length=50, choices=ALCOHOL_TYPE_CHOICES, null=True, blank=True)
#     amount = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)


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
