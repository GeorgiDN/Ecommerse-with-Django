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
