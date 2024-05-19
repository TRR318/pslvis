# Generated by Django 5.0.6 on 2024-05-19 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_experiment_id_alter_subject_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="pslparam",
            name="name",
            field=models.CharField(blank=True, default="current", max_length=100),
        ),
        migrations.AlterField(
            model_name="experiment",
            name="id",
            field=models.SlugField(
                default="ViOtw-pNBM4", editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="subject",
            name="id",
            field=models.SlugField(
                default="zu5rxPOOWhc", editable=False, primary_key=True, serialize=False
            ),
        ),
    ]