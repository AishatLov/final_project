from django.urls import path
from . import views

urlpatterns = [
    path('user/learning-plan/', views.UserLearningPlanView.as_view(), name='user-learning-plan'),
    path('user/ongoing-courses/', views.UserOngoingCoursesView.as_view(), name='user-ongoing-courses'),
    path('user/course-rewards/', views.UserCourseRewardsView.as_view(), name='user-course-rewards'),
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('resources/', views.CourseResourceView.as_view(), name='course-resource'),
    
    # New URLs for quiz functionality
    path('quizzes/', views.QuizListView.as_view(), name='quiz-list'),
    path('quizzes/submit-response/', views.SubmitQuizResponseView.as_view(), name='submit-quiz-response'),
    path('support/tickets/', views.SupportTicketView.as_view(), name='support-tickets'),
    path('schedules/', views.ScheduleView.as_view(), name='schedules'),
]