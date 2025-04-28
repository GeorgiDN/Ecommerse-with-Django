import datetime

from django.shortcuts import render, redirect

from ecommerseApp.accounts.models import Profile
from ecommerseApp.cart.cart import Cart
from ecommerseApp.payment.forms import ShippingForm, PaymentForm
from ecommerseApp.payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from ecommerseApp.payment.utils import create_order, create_order_item, delete_order, update_order_status


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
        phone = my_shipping['shipping_phone']

        shipping_address = (f"{my_shipping['shipping_address1']}\n"
                            f"{my_shipping['shipping_address2']}\n"
                            f"{my_shipping['shipping_city']}\n"
                            f"{my_shipping['shipping_state']}\n"
                            f"{my_shipping['shipping_zip']}\n"
                            f"{my_shipping['shipping_country']}\n")

        amount_paid = totals

        if request.user.is_authenticated:
            user = request.user
            order_created = create_order(full_name, email, phone, shipping_address, amount_paid, user=user)
            order_created.save()
            order_id = order_created.pk
            create_order_item(cart_products, quantities, order_id, user=user)
            # order_item_created.save()
            delete_order(request)

            current_user = Profile.objects.filter(user_id=request.user.id)
            current_user.update(old_cart='')

        else:
            order_created = create_order(full_name, email, phone, shipping_address, amount_paid)
            order_created.save()
            order_id = order_created.pk
            create_order_item(cart_products, quantities, order_id)
            # order_item_created.save()
            delete_order(request)

        messages.success(request, 'Ordered placed test')
        return redirect('home')
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True).order_by('-pk')
        if request.method == 'POST':
            update_order_status(request, shipped=True)
            return redirect('shipped_dash')

        context = {
            'orders': orders,
        }
        return render(request, 'payment/shipped_dash.html', context)
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False).order_by('-pk')
        if request.method == 'POST':
            update_order_status(request, shipped=False)
            return redirect('not_shipped_dash')

        context = {
            'orders': orders,
        }
        return render(request, 'payment/not_shipped_dash.html', context)
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        # items = OrderItem.objects.filter(order=pk)
        products = OrderItem.objects.filter(order=pk)

        if request.method == 'POST':
            status = request.POST['shipping_status']
            order = Order.objects.filter(id=pk)
            if status == 'true':
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order.update(shipped=False)
            messages.success(request, 'Shipping status updated')
            return redirect('home')

        context = {
            'order': order,
            'products': products,
        }
        return render(request, 'payment/orders.html', context)


def payment_success(request):
    return render(request, 'payment/payment_success.html')
