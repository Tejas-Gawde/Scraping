from django.http import JsonResponse
from firebase_admin import firestore
from pathlib import Path
import os
import json


# Create a Firestore client
db = firestore.client()
BASE_DIR = Path(__file__).resolve().parent.parent

json_db = os.path.join(BASE_DIR, 'C:/Users/tejas/Desktop/scraping-assignment/server/nobero_scraper/products.json')


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


def upload_json(request):
    # Load the JSON data from the file
    with open(json_db, 'r') as f:
        data = json.load(f)

    if isinstance(data, list):
        for product in data:
            # Add each product to the 'products' collection in Firestore
            try:
                doc_ref = db.collection('products').add(product)
                print(f"Uploaded: {product.get('title', 'Unknown Product')} with document ID: {doc_ref[1].id}")
            except Exception as e:
                print(f"Failed to upload {product.get('title', 'Unknown Product')}: {e}")
    else:
        print("The data is not in the expected list format.")

