from django.shortcuts import render
from django.views.generic import ListView, DetailView

from ecommerseApp.store.models import Product


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
