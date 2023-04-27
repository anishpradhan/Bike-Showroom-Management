from django.shortcuts import render, get_object_or_404,redirect
from .models import Spareparts, SparepartsReview, SparepartsOrder
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


def spare_parts(request):
    spare_parts = Spareparts.objects.order_by('-created_date')
    paginator = Paginator(spare_parts, 4)
    page = request.GET.get('page')
    paged_parts = paginator.get_page(page)
    brand_search = Spareparts.objects.values_list('brand', flat=True).distinct()
    position_search = Spareparts.objects.values_list(
        'position', flat=True).distinct()

    data = {
        'parts': paged_parts,
        'brand_search': brand_search,
        'position_search': position_search,
    }
    return render(request, 'spareparts/parts.html', data)

def parts_detail(request, id):
    single_part = get_object_or_404(Spareparts, pk=id)
    ratings = SparepartsReview.objects.filter(sparepart_id=id)
    def formatNPR(number):
        s, *d = str(number).partition(".")
        r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d)
    npr_formatted_price = formatNPR(single_part.price)
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
    out_of_stock = False
    if single_part.quantity_available < 1:
        out_of_stock = True    
    context = {
        'single_part': single_part,
        'price': npr_formatted_price,
        'rating_stats': rating_stats,
        'average_rating': average_rating,
        'inactive_rating': 5 - round(average_rating),
        'out_of_stock':  out_of_stock
       
    }
    return render(request, 'spareparts/parts_detail.html', context=context)


def parts_rating(request):
    if request.method == 'POST':
        parts_id = request.POST['parts_id']
        user_id = request.POST['user_id']
        rating = request.POST['rating']
    parts_review = SparepartsReview(sparepart_id=parts_id, user_id=user_id, rating=rating)
    parts_review.save()
    messages.success(request, 'You have successfully rated this spare part.')
    return redirect('/spareparts/'+parts_id)


def parts_search(request):
    spare_parts = Spareparts.objects.order_by('-created_date')
    brand_search = Spareparts.objects.values_list('brand', flat=True).distinct()
    position_search = Spareparts.objects.values_list('position', flat=True).distinct()
   
    search_fields = {}

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            spare_parts = spare_parts.filter(description__icontains=keyword)

    if 'brand' in request.GET:
        brand = request.GET['brand']
        if brand:
            search_fields['brand'] = brand
            spare_parts = spare_parts.filter(model__iexact=brand)

    if 'position' in request.GET:
        position = request.GET['position']
        if position:
            search_fields['position'] = position
            spare_parts = spare_parts.filter(city__iexact=position)
    data = {
        'parts': spare_parts,
        'brand_search': brand_search,
        'position_search': position_search,
        'search_fields': search_fields,
    }

    return render(request, 'spareparts/parts_search.html', data)


def spare_parts_order(request):
    if request.method == 'POST':
        parts_id = request.POST['parts_id']
        user_id = request.POST['user_id']
        quantity = request.POST['quant[1]'] 

    user = User.objects.get(id=user_id)    
    print(quantity)
    spare_parts_order = SparepartsOrder(sparepart_id=parts_id, user=user, quantity=quantity)
    spare_parts_order.save()
    messages.success(request, 'You have successfully purchased this bike. Please wait until we get back to you.')
    return redirect('/spareparts/'+parts_id)   