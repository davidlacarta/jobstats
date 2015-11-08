from celery import Celery
import requests
from .models import Offer

app = Celery('collector')

@app.task
def test():
    url = "http://api.infojobs.net/api/1/offer"
    
    headers = {
        'authorization': "Basic ZTY0NTU1OTY4YTViNDBiYmI0MTcyNGU0OTU1NDg2NmI6UXZGOUg4SFRsSTFtNVg1Q2hoeUs2ZUhEaVRwM0RhN3kzdENHMmMva3BZNFg2SlZwWmI=",
        'cache-control': "no-cache",
        'postman-token': "8eec36b1-0d60-0e4c-f056-cce2173a0f4a"
        }
    
    response = requests.request("GET", url, headers=headers)
    response_json = response.json()
    
    o = response_json['offers'][0]
    salaryMax = o['salaryMax']['value']
    salaryMin = o['salaryMin']['value']
    offer = Offer(poblation=o['city'], 
                    description=o['title'],
                    aplications=int(o['applications']),
                    salary_max=sanity_int(salaryMax),
                    salary_min=sanity_int(salaryMin))
    offer.save()
    
def sanity_int(number):
    return int(number.split(' ')[0].replace('.','') if number else 0) 