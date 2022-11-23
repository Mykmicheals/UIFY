from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import FlexAccount

User = get_user_model()


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        FlexAccount.objects.create(account_owner=instance)
        print(instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     FlexAccount.objects.save()
