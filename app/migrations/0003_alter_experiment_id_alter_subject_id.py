# Generated by Django 5.0.6 on 2024-05-17 13:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_rename_name_experiment_dataset"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experiment",
            name="id",
            field=models.SlugField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="subject",
            name="id",
            field=models.SlugField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
