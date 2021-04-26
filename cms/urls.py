from . import views
from django.urls import path

urlpatterns = [
    path('', views.orders, name="orders"),
]
