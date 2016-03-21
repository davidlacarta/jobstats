import os
import logging
import requests
from celery import Celery
from datetime import timedelta
from django.utils import timezone
from requests.auth import HTTPDigestAuth
from settings import CLIENT_ID, CLIENT_SECRET
from .models import Offer, Provider, Country, Province, City

logger = logging.getLogger(__name__)

app = Celery('collector')

MAX_RESULTS_PER_PAGE = 1000
HOUR = 1920
MONTH = 12
YEAR = 1
ZERO = 0
SALARY_PERIOD = {0: ZERO, 1: HOUR, 2: MONTH, 3: YEAR}
EXPERIENCE_MIN = {0:0, 1:0, 2:1, 6:2, 3:3, 4:4, 5:5, 8:10}
DAYS_FETCH_MIN_UPDATE = 1
DAYS_PUBLISH_MAX_UPDATE = 30
URL_OFFER = 'http://api.infojobs.net/api/1/offer/{}'
URL_ALL = 'http://api.infojobs.net/api/1/offer'

@app.task
def mapping_infojobs():
    logger.debug('Init mapping...')
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    
    provider, _ = Provider.objects.get_or_create(key='infojobs', value='Infojobs')
    id_infojobs = str(provider.id)
    offers_bbdd = Offer.objects.all()
    values = offers_bbdd.values('key','provider_id', 'fetch_date', 'publish_date')
    ids = {(str(v['provider_id']) + v['key']) : [v['fetch_date'], v['publish_date']] for v in values}
    logger.info('Offers in bbdd: {}'.format(len(ids)))
    ids_new = {}
    updates, updates_page, news_page = 0, 0, 0
    
    page, total_pages = 1, 1
    while page <= total_pages:
        params = {'maxResults': MAX_RESULTS_PER_PAGE, 'page': page}
        r = requests.get(URL_ALL, auth=client_auth, params=params)
        response = r.json()
        total_pages = int(response.get('totalPages'))
        logger.debug('Process page: {}/{} ...'.format(page, total_pages))
        if response.get('offers'):
            for offer in response.get('offers'):
                offer_id = offer.get('id')
                key_offer = id_infojobs + offer_id
                try:
                    if key_offer not in ids and key_offer not in ids_new:
                        r_detail = requests.get(URL_OFFER.format(offer_id), auth=client_auth)
                        ids_new[key_offer] = save_offer_detail(r_detail.json(), provider)
                        news_page += 1
                    elif update_required(ids[key_offer][0], ids[key_offer][1]):
                        r_detail = requests.get(URL_OFFER.format(offer_id), auth=client_auth)
                        offer_bbdd = Offer.objects.get(key=offer.get('id'), provider=provider)
                        offer_bbdd.applications = r_detail.json().get('applications')
                        offer_bbdd.update_date = r_detail.json().get('updateDate')
                        offer_bbdd.save()
                        updates_page +=1
                        updates += 1
                except Exception as e:
                    logger.error('{}:{}'.format(key_offer, e))
        logger.debug('Finish page: {}/{}, {} news, {} updates'.format(page, total_pages, news_page, updates_page))
        updates_page, news_page = 0, 0
        page += 1
    logger.info('Finish mapping. {} new offers, {} update offers'.format(len(ids_new), updates))


def update_required(fetch_date, publish_date):
    is_actual = fetch_date + timedelta(days=DAYS_FETCH_MIN_UPDATE) > timezone.now()
    is_old = publish_date + timedelta(days=DAYS_PUBLISH_MAX_UPDATE) < timezone.now()
    return not is_actual and not is_old

        
def save_offer_detail(offer, provider_bbdd):
    provider = provider_bbdd
    # Regions
    country_name = offer.get('country').get('value') if offer.get('country') else ''
    province_name = offer.get('province').get('value') if offer.get('province') else ''
    city_name = offer.get('city', '')
    # Get id bbdd
    country, _ = Country.objects.get_or_create(key=country_name, value=country_name) if country_name else ['','']
    province, _ = Province.objects.get_or_create(key=province_name, value=province_name, country=country) if province_name and country else ['','']
    city, _ = City.objects.get_or_create(key=city_name, value=city_name, province=province) if city_name and province else ['','']
    
    key = offer.get('id')
    title = offer.get('title','')
    description = offer.get('description','')
    requirements = offer.get('minRequirements','') + offer.get('desiredRequirements','')
    link = offer.get('link', '')
    fetch_date = timezone.now()
    publish_date = offer.get('creationDate')
    update_date = offer.get('updateDate')
    experience_min = EXPERIENCE_MIN[offer.get('experienceMin').get('id') if offer.get('experienceMin') else 0]
    applications = offer.get('applications')
    vacancies = offer.get('vacancies', 1)
    
    # Salary
    salary_max = SALARY_PERIOD[offer.get('maxPay').get('periodId')] * offer.get('maxPay').get('amount') if offer.get('maxPay') else 0
    salary_min = SALARY_PERIOD[offer.get('minPay').get('periodId')] * offer.get('minPay').get('amount') if offer.get('minPay') else 0
    
    Offer.objects.create(provider = provider, country = country, 
        province = province, city = city, key = key, title = title, 
        description = description, requirements = requirements, 
        link = link, fetch_date = fetch_date, 
        publish_date = publish_date, update_date = update_date, 
        salary_max = salary_max, salary_min = salary_min, experience_min = experience_min, 
        applications = applications, vacancies = vacancies)
        
    return fetch_date, publish_date
    