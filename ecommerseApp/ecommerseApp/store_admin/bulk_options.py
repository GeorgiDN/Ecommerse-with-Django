from django.contrib import messages
from django.shortcuts import get_object_or_404
from ecommerseApp.store.models import Category


def activate_products(request, products):
    products.update(is_active=True)
    messages.success(request, f"{products.count()} product(s) activated.")


def deactivate_products(request, products):
    products.update(is_active=False)
    messages.success(request, f"{products.count()} product(s) deactivated.")


def delete_products(request, products):
    count = products.count()
    products.delete()
    messages.success(request, f"{count} product(s) deleted.")


def set_available(request, products):
    products.update(is_available=True)
    messages.success(request, f"{products.count()} product(s) are available.")


def set_not_available(request, products):
    products.update(is_available=False)
    messages.success(request, f"{products.count()} product(s) are not available.")


def add_to_category(request, products):
    category_id = request.POST.get('category_id')
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        updated_count = 0
        for product in products:
            product.categories.add(category)
            updated_count += 1
        messages.success(request, f"{updated_count} products added to category '{category.name}'.")


def remove_from_category(request, products):
    category_id = request.POST.get('category_id')
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        updated_count = 0
        for product in products:
            product.categories.remove(category)
            updated_count += 1
        messages.success(request, f"{updated_count} products removed from category '{category.name}'.")


ACTION_HANDLERS = {
    'activate': activate_products,
    'deactivate': deactivate_products,
    'delete': delete_products,
    'is_available': set_available,
    'not_available': set_not_available,
    'add_to_category': add_to_category,
    'remove_from_category': remove_from_category,
}
