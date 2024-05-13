from django.contrib import admin

from .models import Dataset, Experiment, Subject, LogEntry, PslParam, PslResult

for cls in [Dataset, Experiment, Subject, LogEntry, PslParam, PslResult]:
    admin.site.register(cls)