from django.shortcuts import render
import requests

# Create your views here.

def test(request):
    url = "http://api.infojobs.net/api/1/offer"
    
    headers = {
        'authorization': "Basic ZTY0NTU1OTY4YTViNDBiYmI0MTcyNGU0OTU1NDg2NmI6UXZGOUg4SFRsSTFtNVg1Q2hoeUs2ZUhEaVRwM0RhN3kzdENHMmMva3BZNFg2SlZwWmI=",
        'cache-control': "no-cache",
        'postman-token': "8eec36b1-0d60-0e4c-f056-cce2173a0f4a"
        }
    
    response = requests.request("GET", url, headers=headers)

    return render(request, 'index.html', {'response': response.text})