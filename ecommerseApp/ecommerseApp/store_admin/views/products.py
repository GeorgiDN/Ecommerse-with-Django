from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from ecommerseApp.store.models import Product, Category, ProductOption
from ecommerseApp.store_admin.forms import ProductEditForm, ProductCreateForm, ProductOptionFormSet, \
    ProductVariantFormSet, ProductOptionFormSett
from ecommerseApp.store_admin.models_mixins import StaffRequiredMixin
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView, DetailView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from ecommerseApp.store_admin.bulk_options import ACTION_HANDLERS


# class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
#     model = Product
#     form_class = ProductCreateForm
#     template_name = 'store_admin/admin_products/product-create.html'
#
#     def get_success_url(self):
#         return reverse_lazy('admin-products')


class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'store_admin/admin_products/product-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['option_formset'] = ProductOptionFormSet(
                self.request.POST,
                prefix='options'
            )
            context['variant_formset'] = ProductVariantFormSet(
                self.request.POST,
                prefix='variants'
            )
        else:
            context['option_formset'] = ProductOptionFormSet(prefix='options')
            context['variant_formset'] = ProductVariantFormSet(prefix='variants')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        option_formset = context['option_formset']
        variant_formset = context['variant_formset']

        if not (option_formset.is_valid() and variant_formset.is_valid()):
            return self.form_invalid(form)

        self.object = form.save()

        # Save options first
        options = option_formset.save(commit=False)
        for option in options:
            option.product = self.object
            option.save()

        # Now save variants with access to all options
        variants = variant_formset.save(commit=False)
        for variant in variants:
            variant.product = self.object
            variant.save()
            variant_formset.save_m2m()  # Save many-to-many for option_values

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('admin-products')


############
class ProductOptionCreateView(CreateView):
    model = ProductOption
    fields = '__all__'
    template_name = 'store_admin/admin_products/option_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(pk=product_id)

        if self.request.POST:
            context['option_formset'] = ProductOptionFormSett(
                self.request.POST,
                instance=product,
                prefix='options'
            )
        else:
            context['option_formset'] = ProductOptionFormSett(
                instance=product,
                prefix='options'
            )
        context['product'] = product
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        option_formset = context['option_formset']

        if not option_formset.is_valid():
            return self.form_invalid(form)

        product = context['product']
        options = option_formset.save(commit=False)

        for option in options:
            option.product = product
            option.save()

            # Process option values if they exist
            if hasattr(option, 'option_value_formset'):
                value_formset = option.option_value_formset
                if value_formset.is_valid():
                    values = value_formset.save(commit=False)
                    for value in values:
                        value.option = option
                        value.save()

        return redirect('product-detail', pk=product.pk)

    def get_success_url(self):
        product_id = self.kwargs.get('product_id')
        return reverse_lazy('product-detail', kwargs={'pk': product_id})



# class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
#     model = Product
#     form_class = ProductCreateForm
#     template_name = 'store_admin/admin_products/product-create.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['option_formset'] = ProductOptionFormSet(self.request.POST, prefix='options')
#             context['variant_formset'] = ProductVariantFormSet(self.request.POST, prefix='variants')
#         else:
#             context['option_formset'] = ProductOptionFormSet(prefix='options')
#             context['variant_formset'] = ProductVariantFormSet(prefix='variants')
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         option_formset = context['option_formset']
#         variant_formset = context['variant_formset']
#
#         if not (option_formset.is_valid() and variant_formset.is_valid()):
#             return self.form_invalid(form)
#
#         self.object = form.save()
#
#         # Save options and their values
#         options = option_formset.save(commit=False)
#         for option in options:
#             option.product = self.object
#             option.save()
#
#         variants = variant_formset.save(commit=False)
#         for variant in variants:
#             variant.product = self.object
#             variant.save()
#             variant_formset.save_m2m()
#
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('admin-products')


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
