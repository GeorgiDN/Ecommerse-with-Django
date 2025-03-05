from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from ecommerseApp.store.models import Product, Category


def about(request):
    return render(request, 'store/about.html', {})


class ProductListView(ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product


class CategoryListView(ListView):
    model = Category
    template_name = 'store/categories.html'
    context_object_name = 'categories'


class CategoryProductsView(ListView):
    model = Product
    template_name = 'store/category_products_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        category = get_object_or_404(Category, pk=category_id)
        context['category'] = category
        context['products'] = category.category_products.all()
        return context
