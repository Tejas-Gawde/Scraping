from django.http import JsonResponse
from firebase_admin import firestore
from pathlib import Path
import os
import json


# Create a Firestore client
db = firestore.client()



def all_products(request):
    try:
        # Reference the collection
        products_ref = db.collection('products')

        # Get query parameters
        price_range = request.GET.get('price')
        color = request.GET.get('color')
        size = request.GET.get('size')

        # Start building the query based on the parameters
        query = products_ref

        if price_range:
            try:
                min_price, max_price = map(int, price_range.split('-'))
                query = query.where('price', '>=', min_price).where('price', '<=', max_price)
            except ValueError:
                return JsonResponse({'error': 'Invalid price range format'}, status=400)

        if color:
            query = query.where('product_urls.color', '==', color.capitalize())

        if size:
            query = query.where('available_skus.size', 'array_contains', size.upper())

        # Get all documents matching the query
        docs = query.stream()

        # Format the data
        products = []
        for doc in docs:
            product = doc.to_dict()
            products.append(product)

        return JsonResponse({'products': products}, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


