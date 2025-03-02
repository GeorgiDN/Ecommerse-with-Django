from django.shortcuts import render
from ecommerseApp.store.models import Product


def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/home.html', context)


def about(request):

    return render(request, 'store/about.html', {})
