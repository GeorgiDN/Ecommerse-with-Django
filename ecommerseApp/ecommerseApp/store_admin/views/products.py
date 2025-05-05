from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from ecommerseApp.store.models import Product, Category, ProductOption, ProductOptionValue, ProductVariant
from ecommerseApp.store_admin.forms import ProductEditForm, ProductCreateForm, ProductOptionForm, ProductVariantForm
from ecommerseApp.store_admin.models_mixins import StaffRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from ecommerseApp.store_admin.bulk_options import ACTION_HANDLERS


class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'store_admin/admin_products/product-create.html'

    def get_success_url(self):
        return reverse_lazy('admin-products')


class ProductOptionCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = ProductOption
    form_class = ProductOptionForm
    template_name = 'store_admin/admin_products/option_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs['product_id'])
        return context

    def form_valid(self, form):
        product = Product.objects.get(pk=self.kwargs['product_id'])
        option = form.save(commit=False)
        option.product = product
        option.save()

        values = form.cleaned_data.get('values', '')
        if values:
            for value in [v.strip() for v in values.split(',') if v.strip()]:
                ProductOptionValue.objects.create(
                    option=option,
                    value=value
                )

        return redirect(reverse('admin-product-detail', kwargs={'pk': product.pk}))

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.kwargs['product_id']})


class ProductVariantCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = ProductVariant
    form_class = ProductVariantForm
    template_name = 'store_admin/admin_products/variant_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product'] = Product.objects.get(pk=self.kwargs['product_id'])
        return kwargs

    def form_valid(self, form):
        product = Product.objects.get(pk=self.kwargs['product_id'])
        variant = form.save(commit=False)
        variant.product = product
        variant.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin-product-detail', kwargs={'pk': self.kwargs['product_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs['product_id'])
        return context


class AdminProductDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Product
    template_name = 'store_admin/admin_products/admin_product_detail.html'


class ProductEditView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Product
    template_name = 'store_admin/admin_products/product-edit.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('admin-product-detail', kwargs={'pk': self.get_object().pk})


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
                Q(model__icontains=query) |
                Q(tags__icontains=query)
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

        handler = ACTION_HANDLERS.get(action)
        if handler:
            handler(request, products)
        else:
            messages.warning(request, "No valid action selected.")

    return redirect('admin-products')
