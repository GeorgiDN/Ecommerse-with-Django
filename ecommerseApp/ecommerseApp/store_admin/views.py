import csv
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from ecommerseApp.store.models import Product
from ecommerseApp.store_admin.forms import ProductEditForm, ProductCreateForm
from ecommerseApp.store_admin.models_mixins import StaffRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView


class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'store_admin/admin_products/product-create.html'

    def get_success_url(self):
        return reverse_lazy('admin-products')


class ProductEditView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Product
    template_name = 'store_admin/admin_products/product-edit.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.get_object().pk})


class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('admin-products')
    template_name = 'store_admin/admin_products/product_confirm_delete.html'
    success_message = 'Product was deleted.'


class ShopOptionsView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'store_admin/shop-options.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class AdminProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Product
    template_name = 'store_admin/admin_products/admin_product_list.html'
    context_object_name = 'products'


def products_export_csv(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this.")
        return redirect('home')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['id', 'name', 'price', 'description', 'image', 'category_names', 'category_ids', 'is_on_sale', 'sale_price'])

    products = Product.objects.all()
    for product in products:
        category_names = ', '.join([cat.name for cat in product.categories.all()])
        category_ids = ', '.join([str(cat.id) for cat in product.categories.all()])
        writer.writerow([
            product.id,
            product.name,
            product.price,
            product.description,
            product.image.url if product.image else '',
            category_names,
            category_ids,
            product.is_on_sale,
            product.sale_price if product.sale_price else 0,
        ])

    return response
