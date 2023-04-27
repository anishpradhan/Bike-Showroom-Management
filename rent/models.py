from django.db import models
from bike.models import Bike
from django.conf import settings
import datetime
from django.core.exceptions import ValidationError

class Rent(models.Model):
    def Date_validation(value):
        if value < datetime.date.today():
            raise ValidationError("The date cannot be in the past")
    
    location_choices = (
        ('New Baneshwor', 'New Baneshwor'),
        ('Chabahel', 'Chabahel'),
        ('Kalanki', 'Kalanki'),
        ('Koteshwor', 'Koteshwor'),
        ('Gongabu', 'Gongabu'),
        ('Tripureshwor', 'Tripureshwor'),
        ('Baluwatar', 'Baluwatar'),
        ('Kamaladi', 'Kamaladi'),
    )
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='rented_bike')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    dropoff_date = models.DateField()
    location = models.CharField(choices=location_choices, max_length=100)
    rented_date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=0)
    returned_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user.username)+";"+str(self.bike.bike_title)+";"+str(self.pickup_date)+";"+str(self.dropoff_date)

    def save(self, *args, **kwargs):
        date_format = "%Y-%m-%d"
        pickupdate = datetime.datetime.strptime(str(self.pickup_date), date_format)
        dropoffdate = datetime.datetime.strptime(str(self.dropoff_date), date_format)
        self.price = self.bike.rent_price * ((dropoffdate - pickupdate).days + 1)
        super(Rent, self).save(*args, **kwargs)
    class Meta:
        verbose_name = "Rent"
        verbose_name_plural = "Rents"


class RentReview(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='rent_review_bike')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "RentReview"
        verbose_name_plural = "RentReviews"