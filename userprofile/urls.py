from django.urls import path
from .views import SetupProfileView, LoginView, RegisterView, UpdateProfilePictureView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('setup-profile/', SetupProfileView.as_view(), name='setup-profile'),
    path('register/', RegisterView.as_view(), name='register'),  # Corrected
    path('update-profile-picture/', UpdateProfilePictureView.as_view(), name='update-profile-picture'),  # Corrected
    path('profile/', SetupProfileView.as_view(), name='profile'),  # Alias for setup-profile
    # Add more URLs here as needed
]