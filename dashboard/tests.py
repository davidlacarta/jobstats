from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from collector.models import Offer, Province
from dashboard.views import *
from datetime import datetime

# Testing shell django
# $ from django.test import utils
# $ utils.setup_test_environment()
class DashBoardTestcase(TestCase):
    
    fixtures = ['init']
    
    def setUp(self):
        self.c = Client()
        self.offers = Offer.objects.all()
        self.keys = 'word1,word2,word3,word4'
        
    def test_fixtures(self):
        provinces = Province.objects.all()
        self.assertEqual(4, provinces.count())
        self.assertEqual(10, self.offers.count())
        self.assertEqual(3, self.offers.filter(province__key="p1").count())
        self.assertEqual(3, self.offers.filter(province__key="p2").count())
        self.assertEqual(3, self.offers.filter(province__key="p3").count())
        self.assertEqual(1, self.offers.filter(province__key="p4").count())
        self.assertEqual(3, self.offers.filter(title="word1").count())
        self.assertEqual(3, self.offers.filter(title="word2").count())
        self.assertEqual(3, self.offers.filter(title="word3").count())
        self.assertEqual(1, self.offers.filter(title="word4").count())
        
    def test_IndexView(self):
    	response = self.c.get(reverse("dashboard-index"))
    	self.assertEqual(200, response.status_code)
    	
    def test_filter_experience(self):
        s = filter_experience(self.offers, 1, 5)
        self.assertEqual(1, s.count())
        
    def test_filter_regex(self):
        s = filter_regex(self.offers, keys='word1')
        self.assertEqual(3, s.count())
        
    def test_filter_province(self):
        s = filter_provinces(self.offers, 'p1')
        self.assertEqual(3, filter_provinces(self.offers, 'p1').count())
        self.assertEqual(3, filter_provinces(self.offers, 'p2').count())
        self.assertEqual(3, filter_provinces(self.offers, 'p3').count())
        self.assertEqual(1, filter_provinces(self.offers, 'p4').count())
        
    def test_get_provinces_by_oportunity(self):
        s = get_provinces_by_oportunity(self.offers)
        self.assertEqual(('p4', [4.0, 1]),  s[0])
        self.assertEqual(('p1', [3.0, 3]),  s[1])
        self.assertEqual(('p2', [2.0, 3]),  s[2])
        self.assertEqual(('p3', [1.0, 3]),  s[3])
    
    def test_get_provinces_by_salary(self):
        s = get_provinces_by_salary(self.offers)
        self.assertEqual(('p4', [25500.0, 1]),  s[0])
        self.assertEqual(('p1', [22500.0, 3]),  s[1])
        self.assertEqual(('p2', [19500.0, 3]),  s[2])
        self.assertEqual(('p3', [16500.0, 3]),  s[3])
    
    def test_get_regex_by_oportunity(self):
        s = get_regex_by_oportunity(self.offers, self.keys)
        self.assertEqual(('word4', [4.0, 1]),  s[0])
        self.assertEqual(('word1', [3.0, 3]),  s[1])
        self.assertEqual(('word2', [2.0, 3]),  s[2])
        self.assertEqual(('word3', [1.0, 3]),  s[3])
        
    def test_get_regex_by_salary(self):
        s = get_regex_by_salary(self.offers, self.keys)
        self.assertEqual(('word4', [25500.0, 1]),  s[0])
        self.assertEqual(('word1', [22500.0, 3]),  s[1])
        self.assertEqual(('word2', [19500.0, 3]),  s[2])
        self.assertEqual(('word3', [16500.0, 3]),  s[3])