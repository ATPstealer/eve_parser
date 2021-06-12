from django.urls import path

from . import views

urlpatterns = [
    path('', views.eve_pars, name='eve_pars'),
]