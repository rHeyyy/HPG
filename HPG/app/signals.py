from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Owner

@receiver(post_save, sender=Owner)
def update_owner_name(sender, instance, created, **kwargs):
    """
    Automatically populate the 'name' field with the full name of the user
    whenever an Owner instance is created or updated, but prevent recursion.
    """
    if instance.user and not instance.name:
        # Only update the name if it hasn't been populated yet
        instance.name = instance.user.get_full_name()
        instance.save(update_fields=['name'])  # Save only the 'name' field
