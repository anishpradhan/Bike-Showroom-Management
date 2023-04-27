from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField
from django.conf import settings
from django_resized import ResizedImageField

# Create your models here.
class Spareparts(models.Model):

    stock_choices = (
        ('On Stock', 'On Stock'),
        ('Selling Fast', 'Selling Fast'),
        ('Out of Stock', 'Out of Stock'),
    )

    title = models.CharField(max_length=1000)
    description = RichTextField()
    features = RichTextField(blank=True)
    brand = models.CharField(max_length=100)
    compatible_vehicle = models.CharField(max_length=100)
    package_includes = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    stock = models.CharField(choices=stock_choices, max_length=100)
    price = models.IntegerField()
    quantity_available = models.IntegerField()
    parts_photo = ResizedImageField(upload_to='photos/%Y/%m/%d/')
    parts_photo_1 = ResizedImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    parts_photo_2 = ResizedImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    parts_photo_3 = ResizedImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    parts_photo_4 = ResizedImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Sparepart"
        verbose_name_plural = "Spareparts"


class SparepartsReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    sparepart = models.ForeignKey(Spareparts, related_name='reviews',
                                  on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.rating)

    class Meta:
        verbose_name = "Spareparts Review"
        verbose_name_plural = "Spareparts Reviews"


class SparepartsOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    sparepart = models.ForeignKey(Spareparts, related_name='orders',
                                  on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    price = models.IntegerField()

    def __str__(self):
        return str(self.user)+ str(self.sparepart)

    def save(self, *args, **kwargs):
        self.price = int(self.sparepart.price) * int(self.quantity)
        super(SparepartsOrder, self).save(*args, **kwargs)
        remaining_quantity = int(self.sparepart.quantity_available) - int(self.quantity)
        self.sparepart.quantity_available = remaining_quantity
        if remaining_quantity == 0:
            self.sparepart.stock = 'Out of Stock'
        self.sparepart.save()


    class Meta:
        verbose_name = "Spareparts Order"
        verbose_name_plural = "Spareparts Orders"