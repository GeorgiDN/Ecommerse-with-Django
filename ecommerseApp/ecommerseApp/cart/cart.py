import json
from decimal import Decimal
from django.contrib import messages
from django.db.models import Count


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, product, quantity, options=None, variant=None, log_user=None):
        from ecommerseApp.accounts.models import Profile

        product_id = str(product.id)
        product_qty = int(quantity)
        if options is None:
            options = {}

        # Create unique key based on product_id and sorted option value IDs
        sorted_option_ids = "-".join(str(v) for k, v in sorted(options.items()))
        item_key = f"{product_id}:{sorted_option_ids}" if sorted_option_ids else product_id

        if item_key in self.cart:
            if not options:
                if ((not product.is_available) or
                        (product.track_quantity and self.cart[item_key]["quantity"] + product_qty > product.quantity)):
                    return False
                else:
                    self.cart[item_key]["quantity"] += product_qty
            else:
                if ((not product.is_available) or
                        (variant.track_quantity and self.cart[item_key]["quantity"] + product_qty > variant.quantity)):
                    return False
                else:
                    self.cart[item_key]["quantity"] += product_qty

        else:
            if not options:
                if product.track_quantity and product_qty > product.quantity:
                    return False
                else:
                    self.cart[item_key] = {
                        "quantity": product_qty,
                        "options": options
                    }
            else:
                if not log_user and (variant.track_quantity and product_qty > variant.quantity):
                    return False
                else:
                    self.cart[item_key] = {
                        "quantity": product_qty,
                        "options": options
                    }

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", '"')
            current_user.update(old_cart=str(carty))

        return True

    def get_products(self):
        from django.db.models import Count
        from ecommerseApp.store.models import Product, ProductOptionValue, ProductVariant

        product_data = []

        for key, item in self.cart.items():
            product_id = key.split(":")[0]
            product = Product.objects.filter(id=product_id).first()
            if not product:
                continue

            if not isinstance(item, dict):
                item = {"quantity": item, "options": {}}

            option_value_ids = list(item.get("options", {}).values())

            option_values = ProductOptionValue.objects.filter(
                id__in=option_value_ids
            ).select_related("option")

            option_details = [
                {
                    "name": ov.option.name,
                    "value": ov.value
                } for ov in option_values
            ]

            variant = None
            if option_value_ids:
                variant = (
                    ProductVariant.objects
                    .filter(product=product, option_values__in=option_value_ids)
                    .annotate(num_options=Count("option_values"))
                    .filter(num_options=len(option_value_ids))
                    .first()
                )

            product_data.append({
                "key": key,  # <-- Unique key for the item
                "product": product,
                "quantity": item.get("quantity", 1),
                "option_details": option_details,
                "variant": variant,
            })

        return product_data

    def get_quantity(self):
        return sum(
            v if isinstance(v, int) else v.get("quantity", 0)
            for v in self.cart.values()
        )

    def update(self, product, quantity):
        from ecommerseApp.accounts.models import Profile
        from ecommerseApp.store.models import Product, ProductVariant

        product_id = str(product)
        product_qty = int(quantity)
        ourcart = self.cart

        if product_id not in ourcart:
            return False

        # Handle variant case
        if ':' in product_id:
            base_product_id, option_ids = product_id.split(':', 1)

            variant = ProductVariant.objects.filter(
                product_id=base_product_id,
                option_values__id__in=option_ids.split('-')
            ).distinct().first()

            if not variant or (variant.track_quantity and product_qty > variant.quantity):
                return False

        # Handle regular product case
        else:
            product = Product.objects.filter(id=product_id).first()
            if not product or (product.track_quantity and product_qty > product.quantity):
                return False

        # Update quantity if all validations passed
        ourcart[product_id]['quantity'] = product_qty
        self.session.modified = True

        # Update user's cart if authenticated
        if self.request.user.is_authenticated:
            Profile.objects.filter(
                user__id=self.request.user.id
            ).update(old_cart=str(self.cart).replace("'", '"'))

        return True

    def cart_total(self):
        from ecommerseApp.store.models import Product, ProductOptionValue, ProductVariant
        total = Decimal('0.00')

        for key, item in self.cart.items():
            product_id = int(key.split(":")[0])
            product = Product.objects.filter(id=product_id).first()
            if not product:
                continue

            qty = item if isinstance(item, int) else item.get('quantity', 1)
            options = item.get("options", {})

            price = None

            if options:
                option_value_ids = list(map(int, options.values()))

                variant = (
                    ProductVariant.objects
                    .filter(product=product, option_values__in=option_value_ids)
                    .annotate(num_options=Count('option_values'))
                    .filter(num_options=len(option_value_ids))
                    .first()
                )

                if variant:
                    price = variant.sale_price if variant.is_on_sale and variant.sale_price else variant.price
                else:
                    price = product.sale_price if product.is_on_sale else product.price
            else:
                price = product.sale_price if product.is_on_sale else product.price

            if price is not None:
                total += Decimal(price) * int(qty)

        return total

    def delete(self, product):
        from ecommerseApp.accounts.models import Profile

        # Only delete exact match if you're sending 'productID:optionValues'
        if product in self.cart:
            del self.cart[product]

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", '"')
            current_user.update(old_cart=carty)

    def __len__(self):
        return len(self.cart)
