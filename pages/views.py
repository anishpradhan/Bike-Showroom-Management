from django.shortcuts import render, redirect
# from .models import Team
from bike.models import Bike
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    featured_bikes = Bike.objects.order_by(
        '-created_date').filter(is_featured=True)
    all_bikes = Bike.objects.order_by('-created_date')
    model_search = Bike.objects.values_list('model', flat=True).distinct()
    city_search = Bike.objects.values_list('city', flat=True).distinct()
    year_search = Bike.objects.values_list('year', flat=True).distinct()
    body_style_search = Bike.objects.values_list(
        'body_style', flat=True).distinct()
    data = {
        'featured_bikes': featured_bikes,
        'all_bikes': all_bikes,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'pages/home.html', data)


def about(request):

    data = {
    }
    return render(request, 'pages/about.html', data)


def services(request):
    return render(request, 'pages/services.html')

@login_required(login_url = 'login')
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']

        email_subject = 'You have a new message from BikeDealer Website regarding ' + subject
        message_body = 'Name: ' + name + '. Email: ' + email + \
            '. Phone: ' + phone + '. Message: ' + message

        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        send_mail(
            email_subject,
            message_body,
            request.user.email
            [admin_email],
            fail_silently=False,
        )
        messages.success(
            request, 'Thank you for contacting us. We will get back to you shortly')
        return redirect('contact')

    return render(request, 'pages/contact.html')
