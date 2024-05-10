from typing import Any
from django.db import models
from .dataset import Dataset


class Experiment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.ForeignKey(Dataset, verbose_name="Dataset attached to the Experiment", on_delete=models.CASCADE)