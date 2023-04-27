from django.urls import path
from . import views

urlpatterns = [
    path('', views.spare_parts, name='spare_parts'),
    path('<int:id>', views.parts_detail, name='parts_detail'),
    path('parts_rating', views.parts_rating, name='parts_rating'),
    path('parts-search', views.parts_search, name='parts_search'),
    path('spare-parts-order', views.spare_parts_order, name='spare_parts_order'),
]
