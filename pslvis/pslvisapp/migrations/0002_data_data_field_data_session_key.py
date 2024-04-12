# Generated by Django 5.0.4 on 2024-04-12 13:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pslvisapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="data",
            name="data_field",
            field=models.JSONField(
                default=list, help_text="Stores the order of rows as a list of IDs"
            ),
        ),
        migrations.AddField(
            model_name="data",
            name="session_key",
            field=models.CharField(default="0", max_length=40, unique=True),
        ),
    ]
