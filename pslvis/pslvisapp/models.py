from typing import Any
from django.db import models

import pandas as pd


class Data(models.Model):
    session_key = models.CharField(max_length=40, unique=True, default="0")
    data_field = models.JSONField(default=list)

    @property
    def features(self):
        return self.data_field

    def insert_feature(self, feature, pos):
        tmp = self.data_field
        tmp.insert(pos, feature)
        self.data_field = tmp
        self.save()

    def remove_feature(self, feature):
        tmp = self.data_field
        tmp.remove(feature)
        self.data_field = tmp
        self.save()

    def move_feature(self, i,k):
        tmp = self.data_field
        tmp[i], tmp[k] = tmp[k], tmp[i]
        self.data_field = tmp
        self.save()