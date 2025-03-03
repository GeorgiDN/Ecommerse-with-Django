from django.contrib import admin
from django.urls import path, include
from ecommerseApp import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ecommerseApp.store.urls')),
    path('accounts/', include('ecommerseApp.accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
