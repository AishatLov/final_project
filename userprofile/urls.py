from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('onboarding-questions/', views.GetOnboardingQuestions.as_view(), name='onboarding-questions'),  # Corrected
    path('save-question-response/',views.SaveUserQuestionResponse.as_view(),name="save-response"),
    path('setup-profile/', views.SetupProfileView.as_view(), name='setup-profile'),
    path('update-profile-picture/', views.UpdateProfilePictureView.as_view(), name='update-profile-picture'),
    # Add more URLs here as needed
    path('update-profile/', views.ProfileView.as_view(), name='profile'),
    path('topics/', views.TopicView.as_view(), name='topics'),  
]