# Generated by Django 4.0.3 on 2023-10-22 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecordingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('audio_file', models.FileField(upload_to='recordings/')),
                ('transcript', models.TextField(blank=True, null=True)),
            ],
        ),
    ]