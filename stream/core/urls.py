from django.urls import path

from .views import InterviewDetailView, SessionDeleteView, SessionDetailView,UserRegistrationView, UserLoginView, UserLogoutView, home, InterviewCreateView, SessionCreateView, InterviewListView, SessionListView, InterviewDeleteView, SessionCreateForInterviewView, session_frame

app_name = 'core'
urlpatterns = [
    path('home/', home, name='home'),
    path('interview/new/', InterviewCreateView.as_view(), name='interview_create'),
    path('session/new/', SessionCreateView.as_view(), name='session_create'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('interviews/', InterviewListView.as_view(), name='interview_list'),
    path('sessions/', SessionListView.as_view(), name='session_list'),
    path('session/<int:pk>/', SessionDetailView.as_view(), name='session_detail'),
    path('session/<int:pk>/delete/', SessionDeleteView.as_view(), name='session_delete'),
    path('interview/<int:pk>/delete/', InterviewDeleteView.as_view(), name='interview_delete'),
    path('interview/<int:pk>/', InterviewDetailView.as_view(), name='interview_detail'),
    path('interview/<int:interview_pk>/session/new/', SessionCreateForInterviewView.as_view(), name='session_create_for_interview'),
    path('session/<str:session_id>/frame/', session_frame, name='session_frame'),
]