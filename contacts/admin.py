from django.contrib import admin
from .models import Contact

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_id', 'first_name', 'last_name','is_for', 'email', 'title', 'city', 'create_date')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'email', 'bike_title')
    list_per_page = 25

admin.site.register(Contact, ContactAdmin)
