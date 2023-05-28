from django.db import models
import uuid


# Create your models here.


class BaseClass(models.Model):
    record_id = models.UUIDField(primary_key=True, max_length=2048,
                                 default=uuid.uuid4,
                                 help_text='common primary key for all the tables')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CustomFilterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
