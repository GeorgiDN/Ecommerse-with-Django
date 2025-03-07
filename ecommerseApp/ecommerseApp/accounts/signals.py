from django.db.models.signals import post_save
from django.dispatch import receiver
from ecommerseApp.accounts.models import Customer
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.user_profile.save()
