from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from ecommerseApp.store.models import Product, Category, ProductOption, ProductOptionValue, ProductVariant
from ecommerseApp.store_admin.forms import ProductEditForm, ProductCreateForm, ProductOptionForm, ProductVariantForm, \
    ProductOptionEditForm, ProductVariantEditForm
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


class AdminProductDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Product
    template_name = 'store_admin/admin_products/admin_product_detail.html'


class AdminProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Product
    template_name = 'store_admin/admin_products/admin_product_list.html'
    context_object_name = 'products'
    ordering = ('name',)
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
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


class ProductOptionEditView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = ProductOption
    form_class = ProductOptionEditForm
    template_name = 'store_admin/admin_products/option_edit.html'

    def get_object(self, queryset=None):
        product_id = self.kwargs['product_id']
        option_id = self.kwargs['option_id']
        return get_object_or_404(
            ProductOption,
            pk=option_id,
            product_id=product_id
        )

    def form_valid(self, form):
        option = form.save()
        values_text = form.cleaned_data.get('values', '')

        if values_text:
            current_values = set(option.option_values.values_list('value', flat=True))
            new_values = {
                v.strip()
                for line in values_text.split('\n')
                for v in line.split(',')
                if v.strip()
            }

            values_to_delete = current_values - new_values
            if values_to_delete:
                option.option_values.filter(value__in=values_to_delete).delete()

            values_to_add = new_values - current_values
            for value in values_to_add:
                ProductOptionValue.objects.create(option=option, value=value)

            # Keep track of unchanged values (important for variants)
            unchanged_values = current_values & new_values

        messages.success(self.request, 'Option updated successfully')
        return redirect('admin-product-detail', pk=option.product.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context


class ProductOptionDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = ProductOption

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Option deleted successfully')
        return JsonResponse({'status': 'success'})

    def get_success_url(self):
        return reverse('admin-product-detail', kwargs={'pk': self.kwargs['product_id']})


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


class ProductVariantEditView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = ProductVariant
    form_class = ProductVariantEditForm
    template_name = 'store_admin/admin_products/variant_edit.html'

    def get_object(self, queryset=None):
        product_id = self.kwargs['product_id']
        variant_id = self.kwargs['variant_id']
        return get_object_or_404(
            ProductVariant,
            pk=variant_id,
            product_id=product_id
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product'] = self.object.product
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Variant updated successfully')
        return response

    def get_success_url(self):
        return reverse('admin-product-detail', kwargs={'pk': self.object.product.pk})


class ProductVariantDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = ProductVariant

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Variant deleted successfully')
        return JsonResponse({'status': 'success'})

    def get_success_url(self):
        return reverse('admin-product-detail', kwargs={'pk': self.kwargs['product_id']})


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
