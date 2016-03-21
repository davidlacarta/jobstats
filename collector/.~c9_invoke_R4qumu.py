import os
import requests
from django.utils import timezone
from requests.auth import HTTPDigestAuth
from celery import Celery
from .models import Offer, Provider, Country, Province, City
from settings import CLIENT_ID, CLIENT_SECRET 

app = Celery('collector')

MAX_RESULTS_PER_PAGE = 1000

HOUR = 1920
MONTH = 12
YEAR = 1
SALARY_PERIOD = {1: HOUR, 2: MONTH, 3: YEAR}

@app.task
def mapping_infojobs():
    URL = 'http://api.infojobs.net/api/1/offer'
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    
    provider = Provider.objects.get_or_create(key='infojobs')
    id_infojobs = str(provider.values('id')[0]['id'])
    offers_bbdd = Offer.objects.all()
    ids = {(str(value['provider_id']) + value['key']) : value['applications'] for value in offers_bbdd.values('key','provider_id','applications')}
    
    page = 1
    total_pages = 1
    # while page <= total_pages:
    # test
    MAX_RESULTS_PER_PAGE = 5  # 5 resultados por página
    while page <= 3: # 3 páginas (15 ofertas)
        params = {'maxResults': MAX_RESULTS_PER_PAGE, 'page': page}
        r = requests.get(URL, auth=client_auth, params=params)
        response = r.json()
        if response.get('offers'):
            for offer in response.get('offers'):
                key_offer = id_infojobs + offer.get('id')
                if key_offer not in ids:
                    offer_detail = get_offer_detail(offer.get('id'), client_auth)
                    save_offer_detail(offer_detail, provider)
                elif ids[key_offer] != offer.get('applications'):
                    update_offer(offer, provider)
        total_pages = int(response.get('totalPages'))
        page += 1
        
def get_offer_detail(key_offer, client_auth):
    URL = 'http://api.infojobs.net/api/1/offer/' + key_offer
    r = requests.get(URL, auth=client_auth)
    return r.json()
        
def save_offer_detail(offer, provider):
    # Provider
    provider_offer = provider
    
    # Regions
    country = offer.get('country').get('value') if offer.get('country') else ''
    province = offer.get('province').get('value') if offer.get('province') else ''
    city = offer.get('city').get('value') if offer.get('city') else ''
    country_offer, _ = Country.objects.get_or_create(key=country)
    province_offer, _ = Province.objects.get_or_create(key=province, country=country_offer)
    city_offer, _ = City.objects.get_or_create(key=city, province=province_offer)
    
    # Key
    id_offer = offer.get('id')
    
    title_offer = offer.get('title','')
    description_offer = offer.get('description','')
    requirements_offer = offer.get('requirementMin','')
    link_offer = offer.get('link')
    
    fetch_date_offer = timezone.now()
    publish_date_offer = offer.get('creationDate')
    
    # Salary
    salary_max_offer = offer.get('salaryMax').get('value') if offer.get('salaryMax') else ''
    salary_min_offer = offer.get('salaryMin').get('value') if offer.get('salaryMin') else ''
    
    experience_offer = offer.get('experienceMin').get('id') if offer.get('experienceMin') else ''
    applications_offer = offer.get('applications')
    vacancies_offer = offer.get('vacancies')
    
    Offer.objects.create(provider = provider_offer,
        country = country_offer,
        province = province_offer,
        city = city_offer,
        key = id_offer,
        title = title_offer,
        description = description_offer,
        requirements = requirements_offer,
        link = link_offer,
        fetch_date = fetch_date_offer,
        publish_date = publish_date_offer,
        salary_max = salary_max_offer,
        salary_min = salary_min_offer,
        experience = experience_offer,
        applications = applications_offer,
        vacancies = vacancies_offer)
    
def update_offer(offer, provider):
    offer_bbdd = Offer.objects.filter(key=offer.get('id'), provider=provider)[:1]
    offer_bbdd.applications = offer.get('applications')
    offer_bbdd.save()
    

def parse_salary(salary, salary_period):
    out = 0
    try:
        out = int(salary.split(' ')[0].replace('.',''))
        if salary_period in SALARY_PERIOD:
            out *= SALARY_PERIOD[salary_period]
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