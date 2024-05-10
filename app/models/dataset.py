from typing import Any
from django.db import models


class Dataset(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name="Friendly name of the Dataset",max_length=30)
    # a dictionary mapping feature index to friendly feature names
    featurenames = models.JSONField(default=dict)
    filepath = models.CharField(max_length=300)