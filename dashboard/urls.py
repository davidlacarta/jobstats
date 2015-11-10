from django.conf.urls import url
from .views import test, angularapp

urlpatterns = [
    url(r'^$', test),
    url(r'^offers/', angularapp),
]