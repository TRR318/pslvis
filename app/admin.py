from django.contrib import admin
from django.core.exceptions import ValidationError

from .forms import DatasetForm
from .models import Dataset, Experiment, Subject, LogEntry, PslParam, PslResult

for cls in [Experiment, Subject, LogEntry, PslParam, PslResult]:
    admin.site.register(cls)


class DatasetAdmin(admin.ModelAdmin):
    form = DatasetForm

admin.site.register(Dataset, DatasetAdmin)
