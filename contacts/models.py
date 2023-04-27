from django.db import models
from datetime import datetime

# Create your models here.
class Contact(models.Model):

    list_choices = (
        ('Bike', 'Bike'),
        ('Parts', 'Parts')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_for = models.CharField(choices=list_choices, max_length=100)
    item_id = models.IntegerField()
    customer_need = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    user_id = models.IntegerField(blank=True)
    create_date = models.DateTimeField(blank=True, default=datetime.now)

    def __str__(self):
        return self.email
