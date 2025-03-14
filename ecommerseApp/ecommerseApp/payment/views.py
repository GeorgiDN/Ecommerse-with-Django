from django.shortcuts import render, redirect

from ecommerseApp.cart.cart import Cart
from ecommerseApp.payment.forms import ShippingForm, PaymentForm
from ecommerseApp.payment.models import ShippingAddress, Order, OrderItem
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

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        context = {
            'cart_products': cart.get_products(),
            'quantities': cart.get_quantity(),
            'totals': cart.cart_total(),
            'shipping_info': request.POST,
            'billing_form': PaymentForm(),
        }

        return render(request, 'payment/billing_info.html', context)

    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quantity
        totals = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']

        shipping_address = (f"{my_shipping['shipping_address1']}\n"
                            f"{my_shipping['shipping_address2']}\n"
                            f"{my_shipping['shipping_city']}\n"
                            f"{my_shipping['shipping_state']}\n"
                            f"{my_shipping['shipping_zip']}\n"
                            f"{my_shipping['shipping_country']}\n")

        amount_paid = totals

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address,
                                 amount_paid=amount_paid)
            create_order.save()

            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id
                if product.is_on_sale:
                    price = product.price
                else:
                    price = product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user,
                                                      quantity=value, price=price)
                        create_order_item.save()

            # Delete order
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address,
                                 amount_paid=amount_paid)

            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id
                if product.is_on_sale:
                    price = product.price
                else:
                    price = product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value,
                                                      price=price)
                        create_order_item.save()

            # Delete order
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

        messages.success(request, 'Ordered placed test')
        return redirect('home')
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def payment_success(request):
    return render(request, 'payment/payment_success.html')
