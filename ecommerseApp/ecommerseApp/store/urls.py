from django.conf import settings
from django.urls import path
from ecommerseApp.store import views as store_views
from django.conf.urls.static import static

urlpatterns = [
    path('', store_views.ProductListView.as_view(), name='home'),
    path('about', store_views.about, name='about'),
    path('product/<int:pk>/', store_views.ProductDetailView.as_view(), name='product-detail'),
    path('categories/', store_views.CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/', store_views.CategoryProductsView.as_view(), name='category-products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
