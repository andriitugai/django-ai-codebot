from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('suggest', views.suggest, name='suggest'),
    path('info', views.info, name='info')
]