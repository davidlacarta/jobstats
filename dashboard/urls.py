from django.conf.urls import url
from .views import test, angularapp, search

urlpatterns = [
    url(r'^$', test),
    url(r'^offers/', angularapp),
    url(r'^search/', search),
]