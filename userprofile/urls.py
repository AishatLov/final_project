from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('setup-profile/', views.SetupProfileView.as_view(), name='setup-profile'),
    path('register/', views.RegisterView.as_view(), name='register'),  # Corrected
    path('update-profile-picture/', views.UpdateProfilePictureView.as_view(), name='update-profile-picture'),  # Corrected

    # Add more URLs here as needed (Fatimah code)
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('topics/', views.TopicView.as_view(), name='topics'),
]