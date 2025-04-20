from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from ecommerseApp.store.models import Category
from ecommerseApp.store_admin.forms import *
from ecommerseApp.store_admin.models_mixins import StaffRequiredMixin
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView


class AdminCategoryListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Category
    template_name = 'store_admin/admin_categories/admin_category_list.html'
    context_object_name = 'categories'
    ordering = ('name',)
