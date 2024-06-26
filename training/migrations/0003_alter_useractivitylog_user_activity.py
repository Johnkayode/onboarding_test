# Generated by Django 5.0.3 on 2024-03-28 15:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0002_auto_20240324_0908"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useractivitylog",
            name="user_activity",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_activity_log",
                to="training.useractivity",
            ),
        ),
    ]
