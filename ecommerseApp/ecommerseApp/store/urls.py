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
    path('product/<int:product_id>/variant-details/', store_views.get_variant_details, name='get_variant_details'),
    path('favorites/add/<int:product_id>/', store_views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:product_id>/', store_views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', store_views.list_favorites, name='favorites_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
