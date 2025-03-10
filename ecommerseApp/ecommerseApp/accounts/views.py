from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import messages
from ecommerseApp.accounts.forms import UserRegisterForm, UserUpdateForm, CustomerUpdateForm, ChangePasswordForm, \
    LoginForm
from ecommerseApp.accounts.models import Customer
import json

from ecommerseApp.cart.cart import Cart

User = get_user_model()


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been changed!')

                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update-password')
        else:
            form = ChangePasswordForm(current_user)

    else:
        messages.error(request, 'You are not logged in!')
        return redirect('login')

    context = {
        'form': form,
    }

    return render(request, 'accounts/update_password.html', context)


def login_user(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                current_user = Customer.objects.get(user__id=request.user.id)
                save_cart = current_user.old_cart

                if save_cart:
                    converted_cart = json.loads(save_cart)
                    cart = Cart(request)

                    for key, value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)

                messages.success(request, 'You are now logged in!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password!')

    return render(request, 'accounts/login.html', {'form': form})


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)
        messages.success(self.request, 'Your account has been created!')

        return response


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = CustomerUpdateForm(instance=request.user.user_profile)

        context = {
            'u_form': u_form,
            'p_form': p_form,
        }

        return render(request, 'accounts/profile.html', context)

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = CustomerUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(self.request, 'Your profile has been updated!')
            return redirect('profile')

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request, 'accounts/profile.html', context)


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        profile = get_object_or_404(Customer, pk=self.kwargs["pk"])
        return self.request.user == profile.user

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Customer, pk=self.kwargs["pk"])
        return render(request, self.template_name, {'profile': profile})

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Customer, pk=self.kwargs["pk"])
        user = profile.user

        user.delete()
        profile.delete()

        return redirect(self.success_url)
