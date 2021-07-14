from django.urls import path
from . import views


urlpatterns = [
    path('stats', views.stats, name='stats'),
    path('stats2', views.stats2, name='stats2'),
]