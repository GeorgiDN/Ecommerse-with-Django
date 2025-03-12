from django import forms
from ecommerseApp.payment.models import ShippingAddress
from django.contrib.auth import get_user_model
User = get_user_model()


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2',
            'shipping_state', 'shipping_zip', 'shipping_city', 'shipping_country'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'user_profile'):
            profile = user.user_profile

            self.fields['shipping_full_name'].initial = f"{profile.first_name} {profile.last_name}"
            self.fields['shipping_email'].initial = user.email
            self.fields['shipping_address1'].initial = profile.address1
            self.fields['shipping_address2'].initial = profile.address2
            self.fields['shipping_state'].initial = profile.state
            self.fields['shipping_zip'].initial = profile.zip
            self.fields['shipping_city'].initial = profile.city
            self.fields['shipping_country'].initial = profile.country


class PaymentForm(forms.Form):
    card_name = forms.CharField(label="",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name On Card'}),
                                required=True)
    card_number = forms.CharField(label="",
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}),
                                  required=True)
    card_exp_date = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Expiration Date'}), required=True)
    card_cvv_number = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'CVV Code'}), required=True)
    card_address1 = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Address 1'}), required=True)
    card_address2 = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Address 2'}), required=False)
    card_city = forms.CharField(label="",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing City'}),
                                required=True)
    card_state = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing State'}), required=True)
    card_zipcode = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Zipcode'}), required=True)
    card_country = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Country'}), required=True)

