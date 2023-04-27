from django.shortcuts import render, redirect
from .models import Rent, RentReview
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages

def rent(request):
    if request.method == 'POST':
        bike_id = request.POST['bike_id']
        user_id = request.POST['user_id']
        pickup = request.POST['pickup'] 
        date_split = pickup.split(' - ')
        pickup_date = date_split[0]
        dropoff_date = date_split[1]
        location = request.POST['location']

    user = User.objects.get(id=user_id)    

    rented = Rent(bike_id=bike_id, user=user, location=location, pickup_date=pickup_date, dropoff_date=dropoff_date)
    rented.save()
    messages.success(request, 'You have successfully rented the bike. Please wait until we get back to you.')
    return redirect('/bike/'+bike_id)   

def rent_rating(request):
    if request.method == 'POST':
        bike_id = request.POST['bike_id']
        user_id = request.POST['user_id']
        rating = request.POST['rating']
    rent_review = RentReview(bike_id=bike_id, user_id=user_id, rating=rating)
    rent_review.save()
    messages.success(request, 'You have successfully rated the bike.')
    return redirect('/bike/'+bike_id)