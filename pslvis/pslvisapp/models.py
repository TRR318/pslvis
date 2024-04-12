from typing import Any
from django.db import models

import pandas as pd


class Data(models.Model):
    session_key = models.CharField(max_length=40, unique=True, default="0")
    data_field = models.JSONField(default=list)

    @property
    def data(self):
        return list(self.df.itertuples(index=False))

    @property
    def df(self):
        return pd.DataFrame(self.data_field)

    @df.setter
    def df(self, value):
        self.data_field = list(pd.DataFrame(value).itertuples(index=False))
        self.save()
