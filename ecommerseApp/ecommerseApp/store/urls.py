from django.conf import settings
from django.urls import path
from ecommerseApp.store import views as store_views
from django.conf.urls.static import static


urlpatterns = [
    path('', store_views.ProductListView.as_view(), name='home'),
    path('about', store_views.about, name='about'),
    path('categories/', store_views.CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/', store_views.CategoryProductsView.as_view(), name='category-products'),
    path('shop-options', store_views.ShopOptionsView.as_view(), name='shop-options'),
    path('export-products/', store_views.export_products_csv, name='export-products'),
    path('admin-products/', store_views.AdminProductListView.as_view(), name='admin-products'),
    path('product/<int:pk>/', store_views.ProductDetailView.as_view(), name='product-detail'),
    path('product-edit/<int:pk>/', store_views.ProductEditView.as_view(), name='product-edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
