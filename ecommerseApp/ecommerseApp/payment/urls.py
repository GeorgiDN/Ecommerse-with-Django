from django.urls import path
from ecommerseApp.payment import views as p_views

urlpatterns = [
    path('payment_success', p_views.payment_success, name='payment_success'),
    path('checkout', p_views.checkout, name='checkout'),
    path('billing_info', p_views.billing_info, name='billing_info'),
    path('process_order', p_views.process_order, name='process_order'),
    path('shipped_dash', p_views.shipped_dash, name='shipped_dash'),
    path('not_shipped_dash', p_views.not_shipped_dash, name='not_shipped_dash'),
]
