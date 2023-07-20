from django.urls import path
from . import views

urlpatterns = [
    path('liquidity/', views.liquidity, name='liquidity'),
    path('planing/', views.planing, name='planing'),
    path('liquidity/exel', views.exel_liquidity, name='exel_liquidity'),
    path('planing/exel', views.exel_planing, name='exel_planing'),

]
