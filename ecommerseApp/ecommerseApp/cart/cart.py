
class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, product, quantity):
        from ecommerseApp.accounts.models import Customer
        product_id = str(product)
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id] += product_qty
        else:
            self.cart[product_id] = product_qty

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Customer.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        from ecommerseApp.accounts.models import Customer
        product_id = str(product.id)
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id] += product_qty
        else:
            self.cart[product_id] = product_qty

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Customer.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def get_products(self):
        from ecommerseApp.store.models import Product
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantity(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        from ecommerseApp.accounts.models import Customer
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        cart = self.cart

        if self.request.user.is_authenticated:
            current_user = Customer.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

        return cart

    def cart_total(self):
        from ecommerseApp.store.models import Product
        quantities = self.cart
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if not product.is_on_sale:
                        total += int(product.price * value)
                    else:
                        total += int(product.sale_price * value)
        return total

    def delete(self, product):
        from ecommerseApp.accounts.models import Customer
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Customer.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)
