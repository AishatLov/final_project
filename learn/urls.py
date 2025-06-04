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

    # Updated URLs for completed courses tracking
    path('completed-courses/', views.completed_courses, name='completed-courses'),

    # New URLs for tutor management
    path('tutors/', views.list_tutors, name='list-tutors'),            # GET: List all tutors
    path('tutors/create/', views.create_tutor, name='create-tutor'),  # POST: Create a new tutor
    path('user/progress/', views.list_user_progress, name='list-user-progress'),  # GET: List user progress
    path('user/progress/update/', views.update_course_progress, name='update-course-progress'),  # POST: Update progress
    path('sections/<int:section_id>/', views.SectionDetailView.as_view(), name='section-detail'),
    path('sections/', views.SectionListView.as_view(), name='section-list'),
        
    path('courses/<int:course_id>/materials/', views.CourseMaterialListView.as_view(), name='course-material-list'),  # List and create materials
    path('courses/<int:course_id>/materials/<int:material_id>/', views.CourseMaterialDetailView.as_view(), name='course-material-detail'),
]