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
        ['id',
         'url_slug',
         'name',
         'description',
         'meta_title',
         'meta_description',
         'model',
         'sku',
         'tags',
         'price',
         'is_on_sale',
         'sale_price',
         'image',
         'is_available',
         'is_active',
         'track_quantity',
         'quantity',
         'weight',
         'category_names',
         'category_ids',
         ]
    )

    products = Product.objects.all()
    for product in products:
        category_names = ', '.join([cat.name for cat in product.categories.all()])
        category_ids = ', '.join([str(cat.id) for cat in product.categories.all()])
        writer.writerow([
            product.id,
            product.url_slug,
            product.name,
            product.description,
            product.meta_title,
            product.meta_description,
            product.model,
            product.sku,
            product.tags,
            product.price,
            product.is_on_sale,
            product.sale_price if product.sale_price else 0,
            product.image.url if product.image else '',
            product.is_available,
            product.is_active,
            product.track_quantity,
            product.quantity,
            product.weight,
            category_names,
            category_ids,
        ])

    return response
