# Generated by Django 5.0.6 on 2024-06-17 12:50

import app.models.experiment
import app.models.subject
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_pslparam_name_alter_experiment_id_alter_subject_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pslparam',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='id',
            field=models.SlugField(default=app.models.experiment.generate_unique_slug, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subject',
            name='id',
            field=models.SlugField(default=app.models.subject.generate_unique_slug, editable=False, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='PslResult',
        ),
    ]