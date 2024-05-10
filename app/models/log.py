from typing import Any
from django.db import models
from .subject import Subject


class LogEntry(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Subject, verbose_name="Subject for which the log was created", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)
