from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm

from django.views import generic
from django.urls import reverse_lazy
from .models import Interview, Session
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

class SessionCreateForInterviewView(LoginRequiredMixin, generic.CreateView):
    model = Session
    form_class = SessionForm
    template_name = 'core/session_form.html'

    def form_valid(self, form):
        interview = get_object_or_404(Interview, pk=self.kwargs['interview_pk'])
        form.instance.interview = interview
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('core:interview_detail', kwargs={'pk': self.kwargs['interview_pk']})


def home(request):
    return render(request, "core/home.html")
