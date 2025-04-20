import csv
from django.contrib import messages

from django.http import HttpResponse
from ecommerseApp.store.models import Product
from django.shortcuts import redirect


def products_export_csv(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this.")
        return redirect('home')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['id', 'name', 'price', 'description', 'image', 'category_names', 'category_ids', 'is_on_sale', 'sale_price'])

    products = Product.objects.all()
    for product in products:
        category_names = ', '.join([cat.name for cat in product.categories.all()])
        category_ids = ', '.join([str(cat.id) for cat in product.categories.all()])
        writer.writerow([
            product.id,
            product.name,
            product.price,
            product.description,
            product.image.url if product.image else '',
            category_names,
            category_ids,
            product.is_on_sale,
            product.sale_price if product.sale_price else 0,
        ])

    return response
