from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from ecommerseApp.payment.models import Order
from ecommerseApp.payment.models import ShippingAddress
import datetime
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=User)
def create_shipping(sender, instance, created, **kwargs):
    if created:
        ShippingAddress.objects.create(user=instance)


@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        # If the order is now marked as shipped (True), but it was previously False, then update date_shipped."
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now


# def create_shipping(sender, instance, created, **kwargs):
#     if created:
#         user_shipping = ShippingAddress(user=instance)
#         user_shipping.save()
#
#
# post_save.connect(create_shipping, sender=User)
