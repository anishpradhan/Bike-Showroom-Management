from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
# from django.core.mail import send_mail
# from django.contrib.auth.models import User


# Create your views here.
def inquiry(request):
    if request.method == 'POST':
       
        title = request.POST['title']
        user_id = request.POST['user_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        customer_need = request.POST['customer_need']
        city = request.POST['city']
        state = request.POST['state']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        if 'bike_id' in request.POST:
                bike_id = request.POST['bike_id']
                contact = Contact(item_id=bike_id, is_for='Bike', title=title, user_id=user_id,
        first_name=first_name, last_name=last_name, customer_need=customer_need, city=city,
        state=state, email=email, phone=phone, message=message)
                contact.save()
                messages.success(request, 'Your request has been submitted, we will get back to you shortly.')
                return redirect('/bike/'+bike_id)
        if 'parts_id' in request.POST:
                parts_id = request.POST['parts_id']
                contact = Contact(item_id=parts_id, is_for='Parts', title=title, user_id=user_id,
        first_name=first_name, last_name=last_name, customer_need=customer_need, city=city,
        state=state, email=email, phone=phone, message=message)
                contact.save()
                messages.success(request, 'Your request has been submitted, we will get back to you shortly.')
                return redirect('/spareparts/'+parts_id)
        # if request.user.is_authenticated:
        #     user_id = request.user.id
        #     has_contacted = Contact.objects.all().filter(car_id=car_id, user_id=user_id)
        #     if has_contacted:
        #         messages.error(request, 'You have already made an inquiry about this car. Please wait until we get back to you.')
        #         return redirect('/cars/'+car_id)

        

        # admin_info = User.objects.get(is_superuser=True)
        # admin_email = admin_info.email
        # send_mail(
        #         'New Car Inquiry',
        #         'You have a new inquiry for the car ' + car_title + '. Please login to your admin panel for more info.',
        #         'harribdhr@gmail.com',
        #         [admin_email],
        #         fail_silently=False,
        #     )

        
