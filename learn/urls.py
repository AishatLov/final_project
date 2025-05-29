from django.urls import path
from . import views

urlpatterns = [
    path('user/learning-plan/', views.UserLearningPlanView.as_view(), name='user-learning-plan'),
    path('user/ongoing-courses/', views.UserOngoingCoursesView.as_view(), name='user-ongoing-courses'),
    path('user/course-rewards/', views.UserCourseRewardsView.as_view(), name='user-course-rewards'),
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('resources/', views.CourseResourceView.as_view(), name='course-resource'),
]