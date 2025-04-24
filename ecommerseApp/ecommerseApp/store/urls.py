from django.conf import settings
from django.urls import path
from ecommerseApp.store import views as store_views
from django.conf.urls.static import static


urlpatterns = [
    path('about', store_views.about, name='about'),
    path('', store_views.ProductListView.as_view(), name='home'),
    path('products/<slug:slug>/', store_views.ProductDetailView.as_view(), name='product-detail'),
    path('categories/', store_views.CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>/', store_views.CategoryProductsView.as_view(), name='category-products'),
    path('category-detail/<slug:slug>/', store_views.CategoryDetailView.as_view(), name='category-detail'),
    path('product/<int:product_id>/variant-price/', store_views.get_variant_price, name='get_variant_price'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
