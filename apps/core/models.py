from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(db_column='CreatedAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='UpdatedAt', auto_now=True)
    deleted_at = models.DateTimeField(db_column='DeletedAt' ,blank=True, null=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        # Override delete method to mark the object as logically deleted
        self.deleted_at = timezone.now()
        self.save()

    def is_deleted(self):
        # Check if the record is soft deleted
        return self.deleted_at is not None


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

objects = SoftDeleteManager()
