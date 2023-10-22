from django import forms
from .models import Interview, Session
import os


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['job_title', 'job_description', 'resume']

        def clean_resume(self):
            resume = self.cleaned_data.get('resume')
            ext = os.path.splitext(resume.name)[1]  # [0] returns path+filename
            valid_extensions = ['.pdf', '.doc', '.docx']
            if not ext.lower() in valid_extensions:
                raise forms.ValidationError('Unsupported file extension. Supported file extensions are .pdf, .doc, or .docx')
            return resume

        
class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['interview', 'questions']
