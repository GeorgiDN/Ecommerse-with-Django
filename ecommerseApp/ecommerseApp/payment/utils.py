from ecommerseApp.payment.models import Order, OrderItem
from django.contrib import messages
import datetime

from ecommerseApp.store.models import Product


def create_order(full_name, email, phone, shipping_address, amount_paid, user=None):
    if user:
        order_created = Order(user=user, full_name=full_name, email=email, phone=phone, shipping_address=shipping_address,
                              amount_paid=amount_paid)
        order_created.save()
    else:
        order_created = Order(full_name=full_name, email=email, phone=phone, shipping_address=shipping_address,
                              amount_paid=amount_paid)
    return order_created


def create_order_item(cart_products, quantities, order_id, user=None):
    order_item_created = None

    for item in cart_products():
        product_id = item['key'].split(":")[0]
        product = Product.objects.filter(id=product_id).first()
        price = product.price

        quantity = item['quantity']
        variant = item.get('variant')  # This is a ProductVariant instance or None
        option_details = item.get('option_details', [])

        order_item_created = OrderItem(
            order_id=order_id,
            product=product,
            quantity=quantity,
            price=price,
            user=user if user else None
        )

        # Add variant if available
        if variant:
            order_item_created.variant = variant

        # If you have a field to store option details as JSON/text
        if option_details:
            order_item_created.option_details = option_details

        order_item_created.save()

    return order_item_created

# def create_order_item(cart_products, quantities, order_id, user=None):
#     order_item_created = None
#
#     for item in cart_products():
#         product_id = item['key'].split(":")[0]
#         product = Product.objects.filter(id=product_id).first()
#         if product.is_on_sale:
#             price = product.price
#         else:
#             price = product.price
#
#         quantity = item['quantity']
#         if user:
#             order_item_created = OrderItem(order_id=order_id, product_id=product_id, user=user,
#                                            quantity=quantity, price=price)
#             order_item_created.save()
#         else:
#             order_item_created = OrderItem(order_id=order_id, product_id=product_id,
#                                            quantity=quantity, price=price)
#             order_item_created.save()
#     return order_item_created


# def create_order_item(cart_products, quantities, order_id, user=None):
#     order_item_created = None
#
#     for item in cart_products():
#         product_id = item['key'].split(":")[0]
#         product = Product.objects.filter(id=product_id).first()
#         if product.is_on_sale:
#             price = product.price
#         else:
#             price = product.price
#
#         for key, value in quantities().items():
#             if int(key) == product.id:
#                 if user:
#                     order_item_created = OrderItem(order_id=order_id, product_id=product_id, user=user,
#                                                    quantity=value, price=price)
#                 else:
#                     order_item_created = OrderItem(order_id=order_id, product_id=product_id,
#                                                    quantity=value, price=price)
#     return order_item_created


def delete_order(request):
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]


def update_order_status(request, shipped):
    if request.method == 'POST':
        num = request.POST['num']
        order = Order.objects.filter(pk=num)
        if shipped:
            order.update(shipped=False)
        else:
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
        messages.success(request, 'Shipping status updated')
