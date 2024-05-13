from typing import Any
from django.db import models


class Dataset(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    friendlyname = models.CharField(verbose_name="Friendly name of the Dataset",max_length=30)
    featurenames = models.JSONField(verbose_name="Friendly feature names as a json-list", default=list)
    filepath = models.FileField(verbose_name="Dataset as csv. First column must be target", upload_to="dataset/")

