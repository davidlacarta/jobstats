from django.shortcuts import render
from collector.models import Offer
from django.db.models import Avg
from django.db.models import Max
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core import serializers

MAX_RESULTS = 10

def index(request):
    return render(request, 'index.html')
    
def search(request):
    if request.is_ajax():
        search = request.GET['search']
        data = []
        if search:
            offers = Offer.objects.filter(title__iregex=r'{}'.format(search))
            average = offers.aggregate(Avg('salary_max'))['salary_max__avg']
            offer_max = offers.aggregate(Max('salary_max'))['salary_max__max']
            cities = offers.values('city').order_by().annotate(Count('city'))
            city_max = cities[0]['city']
            items = serializers.serialize("json", offers[:MAX_RESULTS])
            summary = {'count': len(offers), 'average': average, 'max': offer_max, 'city': city_max}
        return JsonResponse({'items': items, 'summary': summary})