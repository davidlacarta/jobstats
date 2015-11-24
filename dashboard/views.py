from django.shortcuts import render
from collector.models import Offer
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core import serializers

MAX_RESULTS = 20

def index(request):
    offers = Offer.objects.all()
    return render(request, 'index.html', {'offers': offers[:MAX_RESULTS]})
    
def search(request):
    return render(request, 'search.html')
    
def angularapp(request):
    if request.is_ajax():
        search = request.GET['search']
        data = []
        if search:
            offers = Offer.objects.filter(title__iregex=r'{}'.format(search))
            data = serializers.serialize("json", offers[:MAX_RESULTS])
        return JsonResponse({'search_offers': data})
    else:
        return redirect('/')