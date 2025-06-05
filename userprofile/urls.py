from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('setup-profile/', views.SetupProfileView.as_view(), name='setup-profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('update-profile-picture/', views.UpdateProfilePictureView.as_view(), name='update-profile-picture'),
    path('onboarding-questions/', views.GetOnboardingQuestions.as_view(), name='onboarding-questions'),  # Corrected
    path('save-question-response/',views.SaveUserQuestionResponse.as_view(),name="save-response"),
    # Add more URLs here as needed
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('topics/', views.TopicView.as_view(), name='topics'),  
]