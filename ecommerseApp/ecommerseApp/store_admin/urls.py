from django.conf import settings
from django.urls import path
from ecommerseApp.store_admin import views as admin_views
from django.conf.urls.static import static


urlpatterns = [
    path('admin-products/', admin_views.AdminProductListView.as_view(), name='admin-products'),
    path('product-create/', admin_views.ProductCreateView.as_view(), name='product-create'),
    path('product-edit/<int:pk>/', admin_views.ProductEditView.as_view(), name='product-edit'),
    path('product-delete/<int:pk>/', admin_views.ProductDeleteView.as_view(), name='product-delete'),
    path('shop-options', admin_views.ShopOptionsView.as_view(), name='shop-options'),

    path('products-export-csv/', admin_views.products_export_csv, name='products-export-csv'),

    path('admin-categories/', admin_views.AdminCategoryListView.as_view(), name='admin-categories'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
