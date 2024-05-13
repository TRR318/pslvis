from uuid import uuid4 as uuid
from django.db import models
from .dataset import Dataset


class Experiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid, editable=False)
    name = models.ForeignKey(
        Dataset,
        verbose_name="Dataset attached to the Experiment",
        on_delete=models.CASCADE,
    )
