# Generated by Django 5.1.6 on 2025-02-13 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quotation_requests", "0005_alter_equipment_quotation_request"),
    ]

    operations = [
        migrations.AddField(
            model_name="equipment",
            name="temp_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
