from django.shortcuts import render
from collector.models import Offer, Province
from django.db.models import Avg
from django.db.models import Max
from django.db.models import Sum
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core import serializers
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from django.db.models import F
from fractions import Fraction
import logging

logger = logging.getLogger(__name__)

MAX_RESULTS = 10

DAYS_MIN = 1
DAYS_MAX = 180
EXPERIENCE_MIN = 1
EXPERIENCE_MAX = 10
SPLIT_PATTERN = ','
JOBS = 'java angular node'
PROVINCE = 'Illes Balears'

#############################################
# index.html
#############################################
def index(request):
    offers = Offer.objects.filter(country__key="Espa\xc3\xb1a").count()
    return render(request, 'index.html', {'offers': offers})


#############################################
# typeahead
#############################################
def provinces(request):
    provinces = Province.objects.filter(country__key="Espa\xc3\xb1a")
    response = dict(province=list(provinces.values('key')))
    return JsonResponse(response)

#############################################
# AJAX SEARCH
#############################################
def search(request):
    if request.is_ajax() and request.method == 'GET':
        search = request.GET['search'].encode("utf-8") if 'search' in request.GET else ''
        province = request.GET['province'].encode("utf-8") if 'province' in request.GET else ''
        
        o_spain = Offer.objects.filter(country__key="Espa\xc3\xb1a")
        o_clean = filter_date(o_spain)
        
        if search and province:
            logger.debug('Keys: {}, province: {}'.format(search, province))
            offers_province = filter_provinces(o_clean, province)
            jobs_sal = get_regex_by_salary(offers_province, search)
            jobs_op = get_regex_by_oportunity(offers_province, search)
            return JsonResponse({'jobs_count': offers_province.count(), 'jobs_op': jobs_op, 'jobs_sal': jobs_sal})
        else:
            logger.debug('Keys: {}'.format(search if search else 'ALL'))
            o_regex = filter_regex(o_clean, search) if search else o_clean
            prov_sal = get_provinces_by_salary(o_regex)
            prov_op = get_provinces_by_oportunity(o_regex)
            return JsonResponse({'prov_count': o_regex.count(), 'prov_op': prov_op, 'prov_sal': prov_sal})
                
    return JsonResponse({})

#############################################
# FILTERS
#############################################
def filter_date(offers, days_min=DAYS_MIN, days_max=DAYS_MAX, date=timezone.now()):
    to_date = date - timedelta(days=days_min)
    from_date = date - timedelta(days=days_max)
    return offers.filter(publish_date__range=(from_date, to_date))
    
def filter_experience(offers, exp_min=EXPERIENCE_MIN, exp_max=EXPERIENCE_MAX):
    return offers.filter(experience_min__gte=exp_min, experience_min__lte=exp_max)
    
def filter_regex(offers, keys=JOBS, only_title=True):
    regex = "|".join(keys.split(SPLIT_PATTERN))
    if only_title:
        return offers.filter(title__iregex=r'{}'.format(regex))
    else:
        return offers.filter(Q(title__iregex=r'{}'.format(regex)) | 
                                    Q(description__iregex=r'{}'.format(regex)) | 
                                    Q(requirements__iregex=r'{}'.format(regex)))

def filter_provinces(offers, province):
    return offers.filter(province__key=province)
                                    
def get_provinces_by_oportunity(offers, reverse=True):
    sum1 = offers.values('province__key').annotate(v=Sum('vacancies'),a=Sum('applications'),s=Count(1))
    div1 = {row['province__key'] : [(float(row['v']) / (row['a'])), row['s']] for row in sum1 if row['a'] > 0}
    return sorted(div1.items(), key=lambda x:x[1][0], reverse=reverse)
    
def get_provinces_by_salary(offers, reverse=True):
    cleans = offers.filter(salary_max__gt=0, salary_min__gt=0)
    sum1 = cleans.values('province__key').annotate(ma=Avg('salary_max'),mi=Avg('salary_min'),s=Count(1))
    avg1 = {row['province__key'] : [((float(row['ma']) + float(row['mi'])) / 2), row['s']] for row in sum1}
    return sorted(avg1.items(), key=lambda x:x[1][0], reverse=reverse)
    
def get_regex_by_oportunity(offers, regex=JOBS, reverse=True):
    reg_map = {}
    for r in regex.split(SPLIT_PATTERN):
        o_aux = filter_regex(offers, r)
        reg_map[r] = o_aux.aggregate(v=Sum('vacancies'),a=Sum('applications'),s=Count(1))
    reg_map2 = {k : [(float(v['v']) / float(v['a'])), v['s']] for k,v in reg_map.iteritems() if v['a'] > 0 and v['v'] > 0}
    return sorted(reg_map2.items(), key=lambda x:x[1][0], reverse=reverse)
    
def get_regex_by_salary(offers, regex=JOBS, reverse=True):
    cleans = offers.filter(salary_max__gt=0, salary_min__gt=0)
    reg_map = {}
    for r in regex.split(SPLIT_PATTERN):
        o_aux = filter_regex(cleans, r)
        reg_map[r] = o_aux.aggregate(ma=Avg('salary_max'),mi=Avg('salary_min'),s=Count(1))
    reg_map2 = {k : [((float(v['ma']) + float(v['mi'])) / 2), v['s']] for k,v in reg_map.iteritems() if v['mi'] > 0  and v['ma'] > 0}
    return sorted(reg_map2.items(), key=lambda x:x[1][0], reverse=reverse)
