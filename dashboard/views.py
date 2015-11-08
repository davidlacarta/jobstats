from django.shortcuts import render
import requests
from collector.models import Offer

# Create your views here.

def test(request):
    offers = Offer.objects.all()

    return render(request, 'index.html', {'offers': offers})