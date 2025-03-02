from django.urls import path
from ecommerseApp.store import views as store_views

urlpatterns = [
    path('', store_views.home, name='home'),
]
