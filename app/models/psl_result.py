from typing import Any
from django.db import models
from .dataset import Dataset 


class PslResult(models.Model):
    id = models.BigAutoField(primary_key=True)
    dataset = models.ForeignKey(Dataset, verbose_name="Dataset, model was calculated for", on_delete=models.CASCADE)
    probas = models.JSONField(default=list)
    metrics = models.JSONField(default=dict)