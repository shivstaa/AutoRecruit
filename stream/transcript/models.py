from django.db import models

class RecordingSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='recordings/')
    transcript = models.TextField(blank=True, null=True)