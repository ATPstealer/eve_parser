from django.urls import path
from . import views

urlpatterns = [
    path('', views.liquidity, name='liquidity'),
]
