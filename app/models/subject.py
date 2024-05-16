from uuid import uuid4 as uuid
from django.db import models
from .experiment import Experiment


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid, editable=False)
    experiment = models.ForeignKey(
        Experiment,
        verbose_name="Experiment this subject is part of",
        on_delete=models.CASCADE,
    )

    @property
    def last_model(self):
        models = self.models.order_by("-updated_at")
        if models:
            return models[0]
        model = PslParam.objects.create(subject=self)
        return model
    
    @property
    def dataset(self):
        return self.experiment.dataset
    
    def __str__(self):
        return f"Subject {self.id} @ {self.experiment.internal_name} - {self.experiment.id}"


class PslParam(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(
        Subject,
        verbose_name="Subject for which the log was created",
        on_delete=models.CASCADE,
        related_name="models",
    )
    _features = models.JSONField(default=list)
    _scores = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, value):
        if value is None:
            self._features = []
        else:
            self._features = value
        self.save()

    @property
    def scores(self):
        return {int(k): v for k, v in self._scores.items()}

    @scores.setter
    def scores(self, value):
        if value is None:
            self._scores = {}
        else:
            self._scores = value
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
        self.features = None
        self.scores = None
