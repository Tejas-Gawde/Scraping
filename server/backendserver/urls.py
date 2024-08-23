from backendserver import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('upload-json-to-db', views.upload_json, name='upload_json'),
    path('/all-products', views.all_products, name='all_products'),
]
