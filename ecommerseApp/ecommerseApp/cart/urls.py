from django.conf import settings
from django.urls import path
from ecommerseApp.cart import views as cart_views
from django.conf.urls.static import static

urlpatterns = [
    path('', cart_views.cart_summary, name='cart_summary'),
    path('add', cart_views.cart_add, name='cart_add'),
    path('update', cart_views.cart_update, name='cart_update'),
    path('delete', cart_views.cart_delete, name='cart_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
