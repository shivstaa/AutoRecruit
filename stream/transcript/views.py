from django.shortcuts import render
from .models import RecordingSession

def index(request):
    return render(request, 'transcript/index.html')

def recording_view(request):
    sessions = RecordingSession.objects.all()
    return render(request, 'transcript/recording.html', {'sessions': sessions})
