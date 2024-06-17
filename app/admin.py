from django.contrib import admin

from .forms import DatasetForm
from .models import Dataset, Experiment, Subject, LogEntry, PslParam

for cls in [Experiment, Subject, LogEntry, PslParam]:
    admin.site.register(cls)


class DatasetAdmin(admin.ModelAdmin):
    form = DatasetForm


admin.site.register(Dataset, DatasetAdmin)
