from django.shortcuts import render, redirect

from ecommerseApp.cart.cart import Cart
from ecommerseApp.payment.forms import ShippingForm
from ecommerseApp.payment.models import ShippingAddress
from django.contrib import messages


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantity()
    totals = cart.cart_total()

    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
    }

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        context['shipping_form'] = shipping_form
        return render(request, 'payment/checkout.html', context)
    else:
        shipping_form = ShippingForm(request.POST or None)
        context['shipping_form'] = shipping_form
        return render(request, 'payment/checkout.html', context)


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quantity()
        totals = cart.cart_total()

        context = {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
        }

        if request.user.is_authenticated:
            context['shipping_info'] = request.POST
            return render(request, 'payment/billing_info.html', context)
        else:
            ...

        shipping_form = ShippingForm(request.POST or None)
        context['shipping_form'] = shipping_form
        return render(request, 'payment/billing_info.html', context)
    else:
        messages.success(request, 'Acces Denied')
        return redirect('home')


def payment_success(request):
    return render(request, 'payment/payment_success.html')
