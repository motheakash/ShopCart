from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from django.utils.text import slugify


@receiver(post_save, sender=Product)
def set_product_slug(sender, instance, created, **kwargs):
    if created:
        # Generate slug from product_id, brand, and name
        instance.slug = f"{instance.product_id}-{slugify(instance.brand)}-{slugify(instance.name)}"
        instance.save()  # Save the instance to update the slug
