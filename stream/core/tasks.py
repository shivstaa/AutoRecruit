# tasks.py

from django_q.tasks import async_task
from core.models import Analysis, Session


def run_analysis(analysis_id):
    analysis = Analysis.objects.get(pk=analysis_id)
    # Your analysis logic here
    analysis.comments = "Your analysis comments"
    analysis.scores = {"score1": 90, "score2": 85}
    analysis.status = 'completed'
    analysis.save()

def start_analysis(session_id):
    session = Session.objects.get(pk=session_id)
    # Your analysis logic here
    # Save the analysis results to the session or a related model
