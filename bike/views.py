from django.shortcuts import render, get_object_or_404, redirect
from .models import Bike, BikeOrder
from rent.models import Rent
from django.core.paginator import Paginator
from rent.models import RentReview
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages

# Create your views here.


def bikes(request):
    bikes = Bike.objects.filter(for_sale=True).order_by('-created_date')
    paginator = Paginator(bikes, 4)
    page = request.GET.get('page')
    paged_bikes = paginator.get_page(page)
    model_search = Bike.objects.values_list('model', flat=True).distinct()
    city_search = Bike.objects.values_list('city', flat=True).distinct()
    year_search = Bike.objects.values_list('year', flat=True).distinct()
    body_style_search = Bike.objects.values_list(
        'body_style', flat=True).distinct()

    data = {
        'bikes': paged_bikes,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'bikes/bikes.html', data)


def bike_detail(request, id):
    single_bike = get_object_or_404(Bike, pk=id)
    ratings = RentReview.objects.filter(bike_id=id)
    try:
        BikeOrder.objects.get(bike_id=id)
        
        is_bought = True
    except:
        is_bought = False
    def formatNPR(number):
        s, *d = str(number).partition(".")
        r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d)
    npr_formatted_rent_price = formatNPR(single_bike.rent_price)
    npr_formatted_sales_price = formatNPR(single_bike.price)
    rating_stats = {'Excellent': 0, 'Good': 0, 'Average': 0, 'Poor': 0, 'Terrible': 0, 'Excellent_percent': 0, 'Good_percent': 0, 'Average_percent': 0, 'Poor_percent': 0, 'Terrible_percent': 0}
    total_rating_amount = 0
    for rating in ratings:
        if rating.rating == 5:
            total_rating_amount += 5
            rating_stats['Excellent'] += 1
        elif rating.rating == 4:
            total_rating_amount += 4
            rating_stats['Good'] += 1
        elif rating.rating == 3:
            total_rating_amount += 3
            rating_stats['Average'] += 1
        elif rating.rating == 2:
            total_rating_amount += 2
            rating_stats['Poor'] += 1
        elif rating.rating == 1:
            total_rating_amount += 1
            rating_stats['Terrible'] += 1

    def calc_percent_and_push(title):
        rating_stats[title+'_percent'] = round(
        (rating_stats[title]/len(ratings))*100)
    average_rating = 0
    if len(ratings) > 0:
        average_rating = round(total_rating_amount/len(ratings), 1)
        for i in ['Excellent', 'Good', 'Average', 'Poor', 'Terrible']:
            calc_percent_and_push(i)
        
    rented = Rent.objects.filter(bike=id, returned_date=None)
    data = {
        'single_bike': single_bike,
        'price': npr_formatted_sales_price,
        'rent_price': npr_formatted_rent_price,
        'rating_stats': rating_stats,
        'average_rating': average_rating,
        'inactive_rating': 5 - round(average_rating),  
        'rented': rented,
        'total_rented': len(rented),
        'bought': is_bought,
    }
    return render(request, 'bikes/bike_detail.html', data)


def rent_search(request):
    search_fields = {}
    if 'pickup' in request.GET:
        pickup = request.GET['pickup'] 
        date_split = pickup.split(' - ')
        pickup_date = date_split[0]
        dropoff_date = date_split[1]
        search_fields['pickup'] = pickup
        rent_search = True
        bikes = Bike.objects.filter(for_rent=True).exclude((Q(rented_bike__pickup_date__lte=pickup_date) & Q(rented_bike__dropoff_date__gte=pickup_date)) | (Q(rented_bike__pickup_date__gte=pickup_date) & Q(rented_bike__dropoff_date__lte=dropoff_date)) | (Q(rented_bike__pickup_date__gte=pickup_date) & Q(rented_bike__pickup_date__lte=dropoff_date)), rented_bike__returned_date=None  ).order_by('-created_date')
    else:
        bikes = Bike.objects.filter(for_sale=True).order_by('-created_date')
        rent_search=False
    model_search = Bike.objects.values_list('model', flat=True).distinct()
    city_search = Bike.objects.values_list('city', flat=True).distinct()
    year_search = Bike.objects.values_list('year', flat=True).distinct()
    body_style_search = Bike.objects.values_list(
        'body_style', flat=True).distinct()
    transmission_search = Bike.objects.values_list(
        'transmission', flat=True).distinct()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            bikes = bikes.filter(description__icontains=keyword)

    if 'model' in request.GET:
        model = request.GET['model']
        if model:
            search_fields['model'] = model
            bikes = bikes.filter(model__iexact=model)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            search_fields['city'] = city
            bikes = bikes.filter(city__iexact=city)

    if 'year' in request.GET:
        year = request.GET['year']
        if year:
            search_fields['year'] = year
            bikes = bikes.filter(year__iexact=year)

    if 'body_style' in request.GET:
        body_style = request.GET['body_style']
        if body_style:
            search_fields['body_style'] = body_style
            bikes = bikes.filter(body_style__iexact=body_style)

    if 'transmission' in request.GET:
        transmission = request.GET['transmission']
        if transmission:
            search_fields['transmission'] = transmission
            bikes = bikes.filter(transmission__iexact=transmission)

  
    data = {
        'bikes': bikes,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
        'transmission_search': transmission_search,
        'search_fields': search_fields,
        'rent_search': rent_search,
    }

    return render(request, 'bikes/search.html', data)


def bike_order(request):
    if request.method == 'POST':
        bike_id = request.POST['bike_id']
        user_id = request.POST['user_id']

    user = User.objects.get(id=user_id)    
    spare_parts_order = BikeOrder(bike_id=bike_id, user=user)
    spare_parts_order.save()
    messages.success(request, 'You have successfully purchased this bike. Please wait until we get back to you.')
    return redirect('/bike/'+bike_id)   