class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id] += product_qty  # Add to existing quantity
        else:
            self.cart[product_id] = product_qty  # New item

        self.session.modified = True

    def get_products(self):
        from ecommerseApp.store.models import Product
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantity(self):
        quantities = self.cart
        return quantities

    def __len__(self):
        return len(self.cart)
