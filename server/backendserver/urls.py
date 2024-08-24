from backendserver import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('import-json-to-firestore', views.import_json_to_firestore, name='import_json_to_firestore'),
    path('getproducts', views.all_products, name='all_products'),
    path('ProductDescription/<str:title>', views.get_product_details, name='get_product_details'),
]
