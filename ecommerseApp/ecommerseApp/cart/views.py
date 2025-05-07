from django.shortcuts import render, get_object_or_404, redirect
from ecommerseApp.cart.cart import Cart
from ecommerseApp.store.models import Product, ProductVariant
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantity()
    totals = cart.cart_total()

    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
    }

    return render(request, 'cart/cart_summary.html', context)


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        product = get_object_or_404(Product, id=product_id)

        # Parse options if passed from the form
        options = {}
        for key in request.POST:
            if key.startswith("option_"):
                option_name = key[7:]  # remove 'option_' prefix
                option_value_id = request.POST.get(key)
                if option_value_id:
                    options[option_name] = int(option_value_id)

        if options:
            try:
                variant = ProductVariant.objects.get(
                    product_id=product_id,
                    option_values__in=options.values(),
                )

                if not cart.db_add(product=product, quantity=product_qty, options=options, variant=variant):
                    messages.error(request, "Not enough quantity available.")
                    return JsonResponse({'error': 'Not enough quantity available.'}, status=400)

            except ProductVariant.DoesNotExist:
                # Handle case where variant does not exist or is mismatched
                response = JsonResponse({'error': 'Variant not found or invalid options selected.'})
                response.status_code = 400
                return response

        else:
            if not product.is_available:
                messages.error(request, 'Product is not available.')
                return JsonResponse({'error': 'Product is not available.'}, status=400)

            if not cart.db_add(product=product, quantity=product_qty, options=options):
                messages.error(request, "Not enough quantity available.")
                return JsonResponse({'error': 'Not enough quantity available.'}, status=400)

            cart_quantity = cart.__len__()

            messages.success(request, 'The product has been added to the cart.')
            return JsonResponse({'qty': cart_quantity})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        if not cart.update(product=product_id, quantity=product_qty):
            messages.error(request, "Not enough quantity available.")
            return JsonResponse({'error': 'Not enough quantity available.'}, status=400)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, 'Your cart has been updated.')
        return response

    return redirect('cart_summary')


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_key = request.POST.get('product_id')
        cart.delete(product=str(product_key))

        messages.success(request, 'Item has been deleted from shopping cart.')
        return JsonResponse({'product': product_key})

    return redirect('cart_summary')
