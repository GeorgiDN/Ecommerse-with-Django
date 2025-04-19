import csv
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, UpdateView

from ecommerseApp.common.forms import SearchForm
from ecommerseApp.store.forms import ProductEditForm
from ecommerseApp.store.models import Product, Category
from django.shortcuts import redirect
from django.urls import reverse


def about(request):
    return render(request, 'store/about.html', {})


class ProductListView(ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        """ Ensure search is always performed on home page """
        if 'search_term' in request.GET and request.path != reverse('home'):
            return redirect(f"{reverse('home')}?search_term={request.GET['search_term']}")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search_term')

        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) |
                Q(description__icontains=search_term)
            )

        return queryset


class ProductDetailView(DetailView):
    model = Product


class ProductEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'store/admin/product-edit.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.get_object().pk})

    def test_func(self):
        return self.request.user.is_staff


class CategoryListView(ListView):
    model = Category
    template_name = 'store/categories.html'
    context_object_name = 'categories'


class CategoryProductsView(ListView):
    model = Product
    template_name = 'store/category_products_list.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        category = get_object_or_404(Category, pk=category_id)
        return category.category_products.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        context['category'] = get_object_or_404(Category, pk=category_id)
        return context


class ShopOptionsView(TemplateView):
    template_name = 'store/admin/shop-options.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class AdminProductListView(UserPassesTestMixin, ListView):
    model = Product
    template_name = 'store/admin/admin_product_list.html'
    context_object_name = 'products'

    def test_func(self):
        return self.request.user.is_staff


def export_products_csv(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this.")
        return redirect('home')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'name', 'price', 'description', 'image', 'category_id', 'is_on_sale', 'sale_price'])

    products = Product.objects.all()
    for product in products:
        writer.writerow([
            product.id,
            product.name,
            product.price,
            product.description,
            product.image.url if product.image else '',
            product.is_on_sale,
            product.sale_price if product.sale_price else 0,
        ])

    return response
