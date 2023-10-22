from datetime import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views import View, generic
from django.contrib.auth.forms import UserCreationForm

from django.views import generic
from django.urls import reverse_lazy
from .models import Conversation, Interview, Session
from .forms import InterviewForm, SessionForm  # Assuming you have created forms for Interview and Session
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.shortcuts import get_object_or_404


class InterviewCreateView(LoginRequiredMixin, generic.CreateView):
    model = Interview
    form_class = InterviewForm
    template_name = 'core/interview_form.html'
    success_url = reverse_lazy('core:interview_list')  # Redirect to home page after successful creation

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user field to the currently logged-in user
        return super().form_valid(form)
    
class InterviewDetailView(LoginRequiredMixin, generic.DetailView):
    model = Interview
    template_name = 'core/interview_detail.html'
    context_object_name = 'interview'

class SessionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Session
    template_name = 'core/session_detail.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.object
        conversations = Conversation.objects.filter(session=session).order_by('created_at')
        context['conversations'] = conversations
        return context

class SessionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Session
    form_class = SessionForm
    template_name = 'core/session_form.html'
    success_url = reverse_lazy('core:sessions')  # Redirect to home page after successful creation

class InterviewListView(LoginRequiredMixin, generic.ListView):
    model = Interview
    template_name = 'core/interview_list.html'
    context_object_name = 'interviews'

class SessionListView(LoginRequiredMixin, generic.ListView):
    model = Session
    template_name = 'core/session_list.html'
    context_object_name = 'sessions'

class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = Session
    template_name = 'core/session_confirm_delete.html'
    success_url = reverse_lazy('core:session_list')

class UserRegistrationView(generic.CreateView):
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('core:login')  # Assuming 'login' is the name of your login URL pattern
    template_name = 'core/register.html'

class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'core/login.html'

class UserLogoutView(LogoutView):
    next_page = '/'  # Redirect to home page after logout


class InterviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Interview
    template_name = 'core/interview_confirm_delete.html'
    success_url = reverse_lazy('core:interview_list')

class SessionCreateForInterviewView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        interview = get_object_or_404(Interview, pk=self.kwargs['interview_pk'])
        session = Session.objects.create(
            interview=interview,
        )
        return redirect('core:session_frame', session_id=session.session_id)
    
def session_frame(request, session_id):
    return render(request, 'core/session_frame.html', {'session_id': session_id})





from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def analyze_view(conversation_instance):
    # Your analysis logic here, call the API to get the next question
    # ...
    next_question = "Test NextQuestion"
    ai_conversation = Conversation.objects.create(
        session=conversation_instance.session,
        speaker='ai',
        text=next_question  # Assume next_question is obtained from your analysis
    )

    # Broadcast the new question to TranscriptConsumer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'transcript_group',  # Assuming the group name is 'transcript_group'
        {
            'type': 'send.question',
            'question': next_question
        }
    )
    

def home(request):
    return render(request, "core/home.html")
