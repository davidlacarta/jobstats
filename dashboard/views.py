import requests
from django.shortcuts import render
from collector.models import Offer
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core import serializers

def test(request):
    offers = Offer.objects.all()
    return render(request, 'index.html', {'offers': offers})
    
def angularapp(request):
    if request.is_ajax():
        search = request.GET['search']
        data = []
        if search:
            offers = Offer.objects.filter(description__contains=search)
            data = serializers.serialize("json", offers)
        return JsonResponse({'search_offers': data})
    else:
        return redirect('/')