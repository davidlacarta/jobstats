from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='dashboard-index'),
    url(r'^search/', views.search, name='dashboard-search'),
]