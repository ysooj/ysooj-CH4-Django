from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
]
