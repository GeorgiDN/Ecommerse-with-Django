from django.conf import settings
from django.urls import path
from ecommerseApp.store_admin import views as admin_views
from django.conf.urls.static import static


urlpatterns = [
    path('admin-products/', admin_views.AdminProductListView.as_view(), name='admin-products'),
    path('product-create/', admin_views.ProductCreateView.as_view(), name='product-create'),
    path('admin-product-detail/<int:pk>/', admin_views.AdminProductDetailView.as_view(), name='admin-product-detail'),
    path('product-edit/<int:pk>/', admin_views.ProductEditView.as_view(), name='product-edit'),
    path('product-delete/<int:pk>/', admin_views.ProductDeleteView.as_view(), name='product-delete'),
    path('shop-options', admin_views.ShopOptionsView.as_view(), name='shop-options'),

    path('product/<int:product_id>/options/create/', admin_views.ProductOptionCreateView.as_view(), name='product-options-create'),
    path('product/<int:product_id>/variant/create/', admin_views.ProductVariantCreateView.as_view(), name='product-variant-create'),
    path('product/<int:product_id>/option/<int:option_id>/edit/', admin_views.ProductOptionEditView.as_view(), name='admin-option-edit'),
    path('product/<int:product_id>/variant/<int:variant_id>/edit/', admin_views.ProductVariantEditView.as_view(), name='admin-variant-edit'),

    path('product/<int:product_id>/option/<int:pk>/delete/', admin_views.ProductOptionDeleteView.as_view(), name='admin-option-delete'),
    path('product/<int:product_id>/variant/<int:pk>/delete/', admin_views.ProductVariantDeleteView.as_view(), name='admin-variant-delete'),

    path('products/export/full/', admin_views.export_products_full, name='export-products-full'),
    path('products/import/', admin_views.import_products, name='import-products'),

    # path('products/export/<str:format_type>/', admin_views.products_export, name='products-export'),
    # path('products/export/', admin_views.products_export, name='products-export'),

    path('products/bulk-edit/', admin_views.bulk_edit_products, name='bulk-edit-products'),

    path('admin-categories/', admin_views.AdminCategoryListView.as_view(), name='admin-categories'),
    path('category-create/', admin_views.CategoryCreateView.as_view(), name='category-create'),
    path('admin-category-detail/<int:pk>/', admin_views.AdminCategoryDetailView.as_view(), name='admin-category-detail'),
    path('category-edit/<int:pk>/', admin_views.CategoryEditView.as_view(), name='category-edit'),
    path('category-delete/<int:pk>/', admin_views.CategoryDeleteView.as_view(), name='category-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
