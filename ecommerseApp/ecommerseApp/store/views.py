from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from ecommerseApp.store.models import Product, Category


# def home(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'store/home.html', context)


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
    model = Category
    template_name = 'store/category_products_list.html'
    context_object_name = 'category'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        category = get_object_or_404(Category, pk=category_id)
        return category.category_products.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        context['category'] = get_object_or_404(Category, pk=category_id)
        return context
