from secrets import token_urlsafe
from django.db import models
from .dataset import Dataset


class Experiment(models.Model):
    id = models.SlugField(primary_key=True, default=token_urlsafe(8), editable=False)
    dataset = models.ForeignKey(
        Dataset,
        verbose_name="Dataset attached to the Experiment",
        on_delete=models.CASCADE,
    )

    internal_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.internal_name} - {self.id}"