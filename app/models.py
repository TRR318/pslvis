from typing import Any
from django.db import models

import pandas as pd


class Data(models.Model):
    session_key = models.CharField(max_length=40, unique=True, default="0")
    data_field = models.JSONField(default=list)

    @property
    def features(self):
        return self.data_field["features"]

    @features.setter
    def features(self, value):
        self.data_field["features"] = value
        self.save()

    @property
    def scores(self):
        return {int(k): v for k, v in self.data_field["scores"].items()}

    @scores.setter
    def scores(self, value):
        self.data_field["scores"] = value
        self.save()

    def insert_feature(self, feature, pos):
        tmp = self.features
        tmp.insert(pos, feature)
        self.features = tmp
        tmp = self.scores
        tmp[feature] = 1
        self.scores = tmp

    def remove_feature(self, feature):
        tmp = self.features
        tmp.remove(feature)
        self.features = tmp
        tmp = self.scores
        del tmp[feature]
        self.scores = tmp

    def move_feature(self, from_, to_):
        tmp = self.features
        f = tmp.pop(from_)
        tmp.insert(to_, f)
        self.features = tmp

    def update_score(self, index, new=None, diff=None):
        tmp = self.scores
        if new:
            tmp[index] = new
        if diff:
            tmp[index] = tmp[index] + diff

        self.scores = tmp
