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
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    questions = models.JSONField()  # You could use a TextField if your Django version < 3.1
    responses = models.JSONField()  # You could use a TextField if your Django version < 3.1
    performance_score = models.FloatField(null=True, blank=True)  # assuming score is a float value, set to null if not scored yet

    def __str__(self):
        return f'Session for {self.interview.job_title} on {self.start_time.strftime("%Y-%m-%d %H:%M:%S")}'
