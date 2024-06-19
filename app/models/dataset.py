import pandas as pd
from django.core.exceptions import ValidationError
from django.db import models
from django import forms

# class Dataset(models.Model):
#     name = models.CharField(primary_key=True, max_length=30)
#     friendlyname = models.CharField(verbose_name="Friendly name of the Dataset", max_length=30)
#     featurenames = models.JSONField(verbose_name="Friendly feature names as a json-list", default=list)
#     filepath = models.FileField(verbose_name="Dataset as csv. First column must be target", upload_to="dataset/")

#     def __str__(self):
#         return self.friendlyname
    
#     @property
#     def path(self):
#         return self.filepath.path


class Dataset(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    friendlyname = models.CharField(verbose_name="Friendly name of the Dataset", max_length=30)
    featurenames = models.JSONField(verbose_name="Friendly feature names as a json-list", default=list)
    filecontent = models.JSONField(verbose_name="Dataset content as JSON", default=dict)

    def __str__(self):
        return self.friendlyname

    def clean(self):
        super().clean()
        filecontent = self.filecontent
        if isinstance(filecontent, list) and filecontent:
            df = pd.DataFrame(filecontent)
            n_features = df.shape[1] - 1

            if len(self.featurenames) != n_features:
                raise ValidationError(
                    f"The featurenames list (len={len(self.featurenames)}) must be one shorter than the column count "
                    f"({n_features}) of the CSV. Note that the first column is interpreted as the target variable."
                )

            if not set(df.iloc[:, 0]) <= {0, 1}:
                raise ValidationError("Column one must be the target column and only contain 0 and 1 values")