# Generated by Django 4.2.6 on 2023-10-22 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="analysis_result",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="session",
            name="analysis_status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("processing", "Processing"),
                    ("done", "Done"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="Analysis",
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
                ("status", models.CharField(default="pending", max_length=20)),
                ("comments", models.TextField(blank=True, null=True)),
                ("scores", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "interview",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="core.interview"
                    ),
                ),
            ],
        ),
    ]