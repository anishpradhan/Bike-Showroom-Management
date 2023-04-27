from django.contrib import admin
from .models import Rent, RentReview
# Register your models here.
class RentAdmin(admin.ModelAdmin):
    list_display = ('id', 'bike', 'user', 'location', 'pickup_date', 'dropoff_date', 'rented_date', 'price', 'returned_date')
    list_display_links = ('id', 'bike', 'user')
    search_fields = ('bike', 'user', 'location')
    list_filter = ('user', 'bike', 'returned_date')


class RentReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'bike', 'user', 'rating', 'created_date')
    list_display_links = ('id', 'rating', 'user',)
    search_fields = ('bike', 'user', 'rating')
    list_filter = ('rating',)


admin.site.register(Rent, RentAdmin)
admin.site.register(RentReview, RentReviewAdmin)
