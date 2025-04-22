from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView
from ecommerseApp.common.forms import SearchForm

from ecommerseApp.store.models import Product, Category
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


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
        queryset = super().get_queryset().filter(is_active=True)
        search_term = self.request.GET.get('search_term')

        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(model__icontains=search_term) |
                Q(sku__icontains=search_term)
            )

        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Product, url_slug=slug, is_active=True)


class CategoryListView(ListView):
    model = Category
    template_name = 'store/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        return queryset


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'store/category_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Category, url_slug=slug, is_active=True)


class CategoryProductsView(ListView):
    model = Product
    template_name = 'store/category_products_list.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, url_slug=slug, is_active=True)
        return category.category_products.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        context['category'] = get_object_or_404(Category, url_slug=slug, is_active=True)
        return context
