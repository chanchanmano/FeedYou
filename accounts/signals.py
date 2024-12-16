from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.models import User, UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create profile signal for user creations"""

    user_profile = UserProfile.objects.filter(user=instance).first()
    if not user_profile:
        UserProfile.objects.create(user=instance)
        return

    user_profile.save()


@receiver(pre_save, sender=User)
def pre_save_user_profile(sender, instance, **kwargs):
    pass
