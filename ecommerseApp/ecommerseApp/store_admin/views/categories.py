from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from ecommerseApp.store.models import Category
from ecommerseApp.store_admin.forms import CategoryCreateForm, CategoryEditForm
from ecommerseApp.store_admin.models_mixins import StaffRequiredMixin
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, CreateView, DetailView


class AdminCategoryListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Category
    template_name = 'store_admin/admin_categories/admin_category_list.html'
    context_object_name = 'categories'
    ordering = ('name',)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class AdminCategoryDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Category
    template_name = 'store_admin/admin_categories/admin_category_detail.html'


class CategoryCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'store_admin/admin_categories/category_create.html'

    def get_success_url(self):
        return reverse_lazy('admin-categories')


class CategoryEditView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryEditForm
    template_name = 'store_admin/admin_categories/category_edit.html'

    def get_success_url(self):
        return reverse('admin-category-detail', kwargs={'pk': self.get_object().pk})


class CategoryDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('admin-categories')
    template_name = 'store_admin/admin_categories/category_confirm_delete.html'
    success_message = 'Category was deleted.'
