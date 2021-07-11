from django.urls import path
from . import views

urlpatterns = [
    path('liquidity', views.liquidity, name='liquidity'),
    path('planing', views.planing, name='planing'),
]
