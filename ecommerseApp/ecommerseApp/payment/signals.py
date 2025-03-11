from django.db.models.signals import post_save
from django.dispatch import receiver
from ecommerseApp.accounts.models import Profile
from django.contrib.auth import get_user_model

from ecommerseApp.payment.models import ShippingAddress

User = get_user_model()


@receiver(post_save, sender=User)
def create_shipping(sender, instance, created, **kwargs):
    if created:
        ShippingAddress.objects.create(user=instance)

# def create_shipping(sender, instance, created, **kwargs):
#     if created:
#         user_shipping = ShippingAddress(user=instance)
#         user_shipping.save()
#
#
# post_save.connect(create_shipping, sender=User)
