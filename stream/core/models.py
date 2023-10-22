import datetime
import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Interview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews')
    job_title = models.CharField(max_length=255, blank=False, null=False)
    job_description = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_delete_url(self):
        return reverse('core:interview_delete', kwargs={'pk': self.pk})
    def get_new_session_url(self):
        return reverse('core:session_create_for_interview', kwargs={'interview_pk': self.pk})

    def __str__(self):
        return self.job_title

class Session(models.Model):
    session_id = models.CharField(max_length=32, unique=True, editable=False)  # hash field
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField(auto_now=True)
    questions = models.JSONField(blank=True, null=True)  # You could use a TextField if your Django version < 3.1
    responses = models.JSONField(blank=True, null=True)  # You could use a TextField if your Django version < 3.1
    performance_score = models.FloatField(null=True, blank=True)  # assuming score is a float value, set to null if not scored yet

    def save(self, *args, **kwargs):
        if not self.pk:  # only on the first save
            current_time = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            base_string = f'{self.interview.id}{current_time}'
            self.session_id = hashlib.md5(base_string.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Session for {self.interview.job_title} on {self.start_time.strftime("%Y-%m-%d %H:%M:%S")}'

# In core/models.py
class Conversation(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    speaker = models.CharField(max_length=10)  # 'user' or 'ai'
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Conversation)
def analyze_conversation(sender, instance, created, **kwargs):
    if created and instance.speaker == 'user':
        from core.views import analyze_view
        # Call your core view to perform the analysis
        analyze_view(instance)