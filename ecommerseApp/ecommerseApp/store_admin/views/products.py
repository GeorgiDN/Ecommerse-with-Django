from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from ecommerseApp.store.models import Product
from ecommerseApp.store_admin.forms import ProductEditForm, ProductCreateForm
from ecommerseApp.store_admin.models_mixins import StaffRequiredMixin
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


class AdminProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Product
    template_name = 'store_admin/admin_products/admin_product_list.html'
    context_object_name = 'products'
    ordering = ('name',)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description=query) |
                Q(sku__icontains=query) |
                Q(model__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
