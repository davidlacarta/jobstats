from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class DashBoardTestcase(TestCase):
    
    def setUp(self):
        self.c = Client()
        
    def test_IndexView(self):
    	response = self.c.get(reverse("dashboard-index"))
    	self.assertEqual(200, response.status_code)