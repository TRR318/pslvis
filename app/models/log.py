from typing import Any
from django.db import models
from .subject import Subject


class LogEntry(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Subject, verbose_name="Subject for which the log was created", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)

    def __str__(self):
        return f"Log for {self.subject} with id {self.id} created at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
