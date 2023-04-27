from django.urls import path
from . import views

urlpatterns = [
    path('', views.bikes, name='bike'),
    path('<int:id>', views.bike_detail, name='bike_detail'),
    path('rent-search', views.rent_search, name='rent-search'),
    path('bike-order', views.bike_order, name='bike_order'),
]
