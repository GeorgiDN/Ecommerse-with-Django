from django.shortcuts import render, get_object_or_404
from ecommerseApp.cart.cart import Cart
from ecommerseApp.store.models import Product
from django.http import JsonResponse


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantity()
    context = {
        'cart_products': cart_products,
        'quantities': quantities,
    }

    return render(request, 'cart/cart_summary.html', context)


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        product = get_object_or_404(Product, id=product_id, quantity=product_qty)

        cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()

        # return JsonResponse({'Product Name': product.name})
        return JsonResponse({'qty': cart_quantity})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def cart_update(request):
    pass


def cart_delete(request):
    pass



