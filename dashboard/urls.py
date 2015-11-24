from django.conf.urls import url
from .views import index, angularapp, search

urlpatterns = [
    url(r'^$', index, name='dashboard-index'),
    url(r'^offers/', angularapp, name='dashboard-angularapp'),
    url(r'^search/', search, name='dashboard-search'),
]