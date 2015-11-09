import os
import requests
from requests.auth import HTTPDigestAuth
from celery import Celery
from .models import Offer
from settings import CLIENT_ID, CLIENT_SECRET 

app = Celery('collector')

@app.task
def mapping_offers():
    URL = 'http://api.infojobs.net/api/1/offer'
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    response = requests.get(URL, auth=client_auth)
    response_json = response.json()
    
    for o in response_json['offers']:
        salaryMax = o['salaryMax']['value']
        salaryMin = o['salaryMin']['value']
        offer = Offer(id_supplier=o['id'],
                        poblation=o['city'], 
                        description=o['title'],
                        applications=int(o['applications']),
                        salary_max=sanity_int(salaryMax),
                        salary_min=sanity_int(salaryMin))
        offer.save()
    
def sanity_int(number):
    return int(number.split(' ')[0].replace('.','') if number else 0) 