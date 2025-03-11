from django.urls import path
from ecommerseApp.payment import views as p_views

urlpatterns = [
    path('payment_success', p_views.payment_success, name='payment_success'),
    path('checkout', p_views.checkout, name='checkout'),
]
