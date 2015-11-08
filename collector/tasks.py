from celery import Celery
import requests
from .models import Offer

app = Celery('collector', broker='redis://127.0.0.1:6379/0')

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
                    salary_max=int(salaryMax if salaryMax else 0),
                    salary_min=int(salaryMin if salaryMin else 0))
    offer.save()