import os
import requests
from django.utils import timezone
from requests.auth import HTTPDigestAuth
from celery import Celery
from .models import Offer
from settings import CLIENT_ID, CLIENT_SECRET 

app = Celery('collector')

MAX_RESULTS = 1000

@app.task
def mapping_infojobs():
    URL = 'http://api.infojobs.net/api/1/offer'
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    
    page = 1
    total_pages = 1
    while page <= total_pages:
        params = {'maxResults': MAX_RESULTS, 'page': page}
        r = requests.get(URL, auth=client_auth, params=params)
        response = r.json()
        if response.get('offers'):
            for offer in response.get('offers'):
                save_offer(offer)
        total_pages = int(response.get('totalPages'))
        page += 1
        
                
def save_offer(offer):
    """
    Save offer in database
    """
    offer_id = offer.get('id')
    if offer_id:
        title = offer.get('title','')
        description = ''
        requirements = offer.get('requirementMin','')
        link = offer.get('link','')
        country = ''
        province = offer.get('province').get('value') if offer.get('province') else ''
        city = offer.get('city','')
        publish_date = offer.get('published','')
        salary_max = offer.get('salaryMax').get('value') if offer.get('salaryMax') else ''
        salary_min = offer.get('salaryMin').get('value') if offer.get('salaryMin') else ''
        applications = offer.get('applications')
        vacancies = 1
        experience = offer.get('experienceMin').get('id') if offer.get('experienceMin') else ''
        
        offer = Offer(offer=offer_id,
            title = title,
            description = description,
            requirements = requirements,
            link = link,
            country = country,
            province = province,
            city = city,
            fetch_date = timezone.now(),
            publish_date = publish_date,
            salary_max = parse_salary(salary_max),
            salary_min = parse_salary(salary_min),
            applications = sanity_int(applications),
            vacancies = vacancies,
            experience = sanity_int(experience))
        offer.save()


def parse_salary(salary):
    out = 0
    try:
        out = int(salary.split(' ')[0].replace('.',''))
    except Exception:
        pass
    return out


def sanity_int(integer):
    out = 0
    try:
        out = int(integer)
    except Exception:
        pass
    return out