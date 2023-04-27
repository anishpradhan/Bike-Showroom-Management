from django.urls import path
from . import views

urlpatterns = [
    path('', views.rent, name='rent'),
    path('rent_rating/', views.rent_rating, name='rent_rating'),

]
