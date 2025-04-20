from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from ecommerseApp.store.models import Product
from ecommerseApp.store_admin.models_mixins import StaffRequiredMixin


class ShopOptionsView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'store_admin/shop-options.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context
