from django.urls import path
from .views import UserLearningPlanView, UserOngoingCoursesView, UserCourseRewardsView

urlpatterns = [
    path('user/learning-plan/', UserLearningPlanView.as_view(), name='user-learning-plan'),
    path('user/ongoing-courses/', UserOngoingCoursesView.as_view(), name='user-ongoing-courses'),
    path('user/course-rewards/', UserCourseRewardsView.as_view(), name='user-course-rewards'),
]