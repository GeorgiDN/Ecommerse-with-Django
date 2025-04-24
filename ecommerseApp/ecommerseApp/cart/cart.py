from decimal import Decimal

from django.db.models import Count


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, product, quantity, options=None):
        from ecommerseApp.accounts.models import Profile

        product_id = str(product.id)
        product_qty = int(quantity)

        if options is None:
            options = {}

        if product_id in self.cart:
            if isinstance(self.cart[product_id], dict):
                self.cart[product_id]["quantity"] += product_qty
            else:
                self.cart[product_id] = {
                    "quantity": self.cart[product_id] + product_qty,
                    "options": options
                }
        else:
            self.cart[product_id] = {
                "quantity": product_qty,
                "options": options
            }

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", '"')
            current_user.update(old_cart=str(carty))

    def get_products(self):
        from django.db.models import Count
        from ecommerseApp.store.models import Product, ProductOptionValue, ProductVariant
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_data = []

        for product in products:
            item = self.cart[str(product.id)]

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
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart
        if isinstance(ourcart.get(product_id), dict):
            ourcart[product_id]['quantity'] = product_qty
        else:
            ourcart[product_id] = {'quantity': product_qty, 'options': {}}

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", '"')
            current_user.update(old_cart=str(carty))

        return self.cart

    def cart_total(self):
        from ecommerseApp.store.models import Product, ProductOptionValue, ProductVariant
        total = Decimal('0.00')

        for product_id, item in self.cart.items():
            product_id = int(product_id)
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
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)



    # def cart_total(self):
    #     from ecommerseApp.store.models import Product, ProductOptionValue, ProductVariant
    #
    #     total = 0
    #     for product_id, item in self.cart.items():
    #         product_id = int(product_id)
    #         product = Product.objects.filter(id=product_id).first()
    #         if not product:
    #             continue
    #
    #         # Get quantity
    #         qty = item if isinstance(item, int) else item.get("quantity", 1)
    #
    #         # Check if options exist
    #         options = item.get("options", {})
    #
    #         if options:
    #             option_value_ids = list(map(int, options.values()))
    #
    #             variant = (
    #                 ProductVariant.objects
    #                 .filter(product=product, option_values__in=option_value_ids)
    #                 .annotate(num_options=Count("option_values"))
    #                 .filter(num_options=len(option_value_ids))
    #                 .first()
    #             )
    #
    #             if variant:
    #                 price = variant.sale_price if variant.is_on_sale and variant.sale_price else variant.price
    #                 total += int(price * qty)
    #             else:
    #                 price = product.sale_price if product.is_on_sale else product.price
    #                 total += int(price * qty)
    #         else:
    #             # No variant, use product base price
    #             price = product.sale_price if product.is_on_sale else product.price
    #             total += int(price * qty)
    #
    #     return total

    # def get_products(self):
    #     from ecommerseApp.store.models import Product, ProductOptionValue
    #
    #     product_ids = self.cart.keys()
    #     products = Product.objects.filter(id__in=product_ids)
    #     product_data = []
    #
    #     for product in products:
    #         item = self.cart[str(product.id)]
    #
    #         if not isinstance(item, dict):
    #             item = {"quantity": item, "options": {}}
    #
    #         option_value_ids = item.get("options", {}).values()
    #
    #         option_values = ProductOptionValue.objects.filter(
    #             id__in=option_value_ids
    #         ).select_related("option")
    #
    #         option_details = [
    #             {
    #                 "name": ov.option.name,
    #                 "value": ov.value
    #             } for ov in option_values
    #         ]
    #
    #         product_data.append({
    #             "product": product,
    #             "quantity": item.get("quantity", 1),
    #             "option_details": option_details
    #         })
    #
    #     return product_data
    #

    # def cart_total(self):
    #     from ecommerseApp.store.models import Product, ProductOption, ProductOptionValue, ProductVariant
    #     quantities = self.cart
    #     product_ids = self.cart.keys()
    #     products = Product.objects.filter(id__in=product_ids)
    #
    #     total = 0
    #     for key, value in quantities.items():
    #         key = int(key)
    #         for product in products:
    #             if product.id == key:
    #                 qty = value if isinstance(value, int) else value.get("quantity", 1)
    #                 if not product.is_on_sale:
    #                     total += int(product.price * qty)
    #                 else:
    #                     total += int(product.sale_price * qty)
    #     return total


    # def get_quantity(self):
    #     quantities = self.cart
    #     return quantities

    # def update(self, product, quantity):
    #     from ecommerseApp.accounts.models import Profile
    #     product_id = str(product)
    #     product_qty = int(quantity)
    #
    #     ourcart = self.cart
    #     ourcart[product_id] = product_qty
    #
    #     self.session.modified = True
    #
    #     cart = self.cart
    #
    #     if self.request.user.is_authenticated:
    #         current_user = Profile.objects.filter(user__id=self.request.user.id)
    #         carty = str(self.cart)
    #         carty = carty.replace("\'", "\"")
    #         current_user.update(old_cart=str(carty))
    #
    #     return cart

    # def cart_total(self):
    #     from ecommerseApp.store.models import Product
    #     quantities = self.cart
    #     product_ids = self.cart.keys()
    #     products = Product.objects.filter(id__in=product_ids)
    #     total = 0
    #     for key, value in quantities.items():
    #         key = int(key)
    #         for product in products:
    #             if product.id == key:
    #                 if not product.is_on_sale:
    #                     total += int(product.price * value)
    #                 else:
    #                     total += int(product.sale_price * value)
    #     return total


    # def add(self, product, quantity):
    #     from ecommerseApp.accounts.models import Profile
    #     product_id = str(product.id)
    #     product_qty = int(quantity)
    #
    #     if product_id in self.cart:
    #         self.cart[product_id] += product_qty
    #     else:
    #         self.cart[product_id] = product_qty
    #
    #     self.session.modified = True
    #
    #     if self.request.user.is_authenticated:
    #         current_user = Profile.objects.filter(user__id=self.request.user.id)
    #         carty = str(self.cart)
    #         carty = carty.replace("\'", "\"")
    #         current_user.update(old_cart=str(carty))


    # def db_add(self, product, quantity):
    #     from ecommerseApp.accounts.models import Profile
    #     product_id = str(product)
    #     product_qty = int(quantity)
    #
    #     if product_id in self.cart:
    #         self.cart[product_id] += product_qty
    #     else:
    #         self.cart[product_id] = product_qty
    #
    #     self.session.modified = True
    #
    #     if self.request.user.is_authenticated:
    #         current_user = Profile.objects.filter(user__id=self.request.user.id)
    #         carty = str(self.cart)
    #         carty = carty.replace("\'", "\"")
    #         current_user.update(old_cart=str(carty))

    # def get_products(self):
    #     from ecommerseApp.store.models import Product
    #     product_ids = self.cart.keys()
    #     products = Product.objects.filter(id__in=product_ids)
    #     return products  # <QuerySet [<Product: Strawberry>]>
