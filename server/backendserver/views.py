from django.http import JsonResponse
from firebase_admin import firestore
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage

db = firestore.client()

@require_GET
def all_products(request):
    # Get query parameters
    price_range = request.GET.get('price')
    color = request.GET.get('color')
    size = request.GET.get('size')
    page = int(request.GET.get('page', 1))  # Default to page 1 if not specified
    items_per_page = 12

    # Start with all products
    query = db.collection('products')

    # Apply filters directly to Firestore query
    if price_range:
        min_price, max_price = map(int, price_range.split('-'))
        query = query.where('price', '>=', min_price).where('price', '<=', max_price)

    if color:
        query = query.where('product_urls', 'array_contains_any', [
            {'color': color.lower()}
        ])

    if size:
        query = query.where('available_skus', 'array_contains_any', [
            {'size': size.upper()}
        ])

    # Execute query with pagination
    docs = query.limit(items_per_page).offset((page - 1) * items_per_page).stream()

    # Process results
    products = []
    for doc in docs:
        product = doc.to_dict()

        # Extract only required fields
        filtered_product = {
            'title': product.get('title'),
            'product_urls': product.get('product_urls'),
            'price': product.get('price')
        }
        products.append(filtered_product)

    # Get total number of pages (required for pagination)
    total_docs = query.count().get()

    return JsonResponse({
        'products': list(products),
        'currentPage': page,
    })

def get_product_details(request, title):
    title = title.replace('-', ' ')
    doc_ref = db.collection('products').where('title', '==', title).limit(1).stream()
    for doc in doc_ref:
        product = doc.to_dict()
        return JsonResponse(product)

def load_json_data(file_path):
    """Helper function to load JSON data from a file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

@require_GET
def import_json_to_firestore(request):
    try:
        # Path to your JSON file
        json_file_path = 'C:/Users/tejas/Desktop/scraping-assignment/server/nobero_scraper/products.json'
        
        # Load JSON data from the file
        data = load_json_data(json_file_path)

        # Ensure data is a list of dictionaries (or adjust as necessary)
        if not isinstance(data, list):
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        # Import data to Firestore
        for item in data:
            doc_ref = db.collection('products').add(item)

        return JsonResponse({'status': 'success'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)