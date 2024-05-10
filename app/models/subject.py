from typing import Any
from django.db import models
from .experiment import Experiment


class Subject(models.Model):
    id = models.BigAutoField(primary_key=True)
    experiment = models.ForeignKey(Experiment, verbose_name="Experiment this subject is part of", on_delete=models.CASCADE)