from typing import Any
from django.db import models
from .subject import Subject


class PslParam(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Subject, verbose_name="Subject for which the log was created", on_delete=models.CASCADE)
    _features = models.JSONField(default=list)
    _scores = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

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

    def insert_feature(self, feature, pos=None, score=1):
        tmp = self.features
        tmp.insert(len(tmp) if pos is None else pos, feature)
        self.features = tmp
        tmp = self.scores
        tmp[feature] = int(score)
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
    def reset(self):
        self.data_field=dict(features=[], scores={})
        self.save()