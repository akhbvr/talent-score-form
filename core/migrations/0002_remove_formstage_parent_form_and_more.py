# Generated by Django 5.0.4 on 2024-04-15 05:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="formstage",
            name="parent_form",
        ),
        migrations.AlterField(
            model_name="formstage",
            name="form_result",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="form_results",
                to="core.formresult",
            ),
        ),
    ]