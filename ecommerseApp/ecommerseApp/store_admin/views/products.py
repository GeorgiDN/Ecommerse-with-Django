from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from ecommerseApp.store.models import Product, Category
from ecommerseApp.store_admin.forms import ProductEditForm, ProductCreateForm
from ecommerseApp.store_admin.models_mixins import StaffRequiredMixin
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404


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
        context['categories'] = Category.objects.all()
        return context


@staff_member_required
def bulk_edit_products(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_products')

        if not selected_ids:
            messages.warning(request, "No products selected.")
            return redirect('admin-products')

        products = Product.objects.filter(id__in=selected_ids)

        if action == 'activate':
            products.update(is_active=True)
            messages.success(request, f"{products.count()} product(s) activated.")
        elif action == 'deactivate':
            products.update(is_active=False)
            messages.success(request, f"{products.count()} product(s) deactivated.")
        elif action == 'delete':
            count = products.count()
            products.delete()
            messages.success(request, f"{count} product(s) deleted.")
        elif action == 'is_available':
            products.update(is_available=True)
            messages.success(request, f"{products.count()} product(s) are available.")
        elif action == 'not_available':
            products.update(is_available=False)
            messages.success(request, f"{products.count()} product(s) are not available.")
        elif action == 'add_to_category':
            category_id = request.POST.get('category_id')
            if category_id:
                category = get_object_or_404(Category, id=category_id)
                updated_count = 0
                for product in Product.objects.filter(id__in=selected_ids):
                    product.categories.add(category)
                    updated_count += 1
                messages.success(request, f"{updated_count} products added to category '{category.name}'.")
        elif action == 'remove_from_category':
            category_id = request.POST.get('category_id')
            if category_id:
                category = get_object_or_404(Category, id=category_id)
                updated_count = 0
                for product in Product.objects.filter(id__in=selected_ids):
                    product.categories.remove(category)
                    updated_count += 1
                messages.success(request, f"{updated_count} products removed from category '{category.name}'.")
        else:
            messages.warning(request, "No valid action selected.")

    return redirect('admin-products')
