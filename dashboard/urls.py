from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='dashboard-index'),
    url(r'^provinces/', views.provinces, name='dashboard-provinces'), # typeahead form
    url(r'^search/', views.search, name='dashboard-search'), # search ajax
]