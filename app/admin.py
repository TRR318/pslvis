from django.contrib import admin

from .models import Dataset, Experiment, Subject, LogEntry

for cls in [Dataset, Experiment, Subject, LogEntry]:
    admin.site.register(cls)