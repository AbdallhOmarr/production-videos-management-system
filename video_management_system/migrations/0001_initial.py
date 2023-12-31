# Generated by Django 4.2.7 on 2023-11-20 12:05

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("video_file", models.FileField(upload_to="videos/")),
                ("product_code", models.CharField(blank=True, max_length=50)),
                ("product_description", models.CharField(blank=True, max_length=255)),
                ("factory", models.CharField(blank=True, max_length=50)),
                ("operation_code", models.CharField(blank=True, max_length=50)),
                ("operation_description", models.CharField(blank=True, max_length=255)),
                ("machine_number", models.CharField(blank=True, max_length=50)),
                ("machine_description", models.CharField(blank=True, max_length=255)),
                ("operator_code", models.CharField(blank=True, max_length=50)),
                ("operator_name", models.CharField(blank=True, max_length=255)),
                ("additional_details", models.TextField(blank=True)),
            ],
        ),
    ]
