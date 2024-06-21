import pandas as pd
from django.core.exceptions import ValidationError
from django.db import models
from django import forms


class Dataset(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    friendlyname = models.CharField(verbose_name="Friendly name of the Dataset", max_length=30)
    featurenames = models.JSONField(verbose_name="Friendly feature names as a json-list", default=list)
    filecontent = models.JSONField(verbose_name="Dataset content as JSON", default=dict)

    def __str__(self):
        return self.friendlyname