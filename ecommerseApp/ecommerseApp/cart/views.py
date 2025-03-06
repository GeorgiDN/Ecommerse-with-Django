from django.shortcuts import render, get_object_or_404
from ecommerseApp.cart.cart import Cart
from ecommerseApp.store.models import Product
from django.http import JsonResponse


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    context = {'cart_products': cart_products}
    return render(request, 'cart/cart_summary.html', context)


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product)

        cart_quantity = cart.__len__()

        # return JsonResponse({'Product Name': product.name})
        return JsonResponse({'qty': cart_quantity})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def cart_update(request):
    pass


def cart_delete(request):
    pass



