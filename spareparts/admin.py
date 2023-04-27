from django.contrib import admin
from .models import Spareparts, SparepartsReview, SparepartsOrder
from django.utils.html import format_html

class SparepartsAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.parts_photo.url))

    thumbnail.short_description = 'Spare Parts Image'
    list_display = ('id','thumbnail','title', 'brand', 'compatible_vehicle', 'stock', 'price', 'quantity_available')
    list_display_links = ('id', 'thumbnail', 'title')
    search_fields = ('id', 'title', 'brand', 'compatible_vehicle')
    list_filter = ('brand', 'stock', 'compatible_vehicle')
admin.site.register(Spareparts, SparepartsAdmin)

class SparepartsReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'sparepart', 'user', 'rating', 'created_date')
    list_display_links = ('id', 'rating', 'user',)
    search_fields = ('sparepart', 'user', 'rating')
    list_filter = ('rating',)

admin.site.register(SparepartsReview, SparepartsReviewAdmin)

class SparepartsOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sparepart', 'quantity', 'price','created_date')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'sparepart')
    list_filter = ('user', 'sparepart')

admin.site.register(SparepartsOrder, SparepartsOrderAdmin)