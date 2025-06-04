from django.urls import path
from . import views

urlpatterns = [
    path('user/learning-plan/', views.user_learning_plans, name='user-learning-plan'),
    path('user/ongoing-courses/', views.user_ongoing_courses, name='user-ongoing-courses'),
    path('user/course-rewards/', views.user_course_rewards, name='user-course-rewards'),
    path('courses/', views.course_list, name='course-list'),
    path('courses/<int:course_id>/', views.course_detail, name='course-detail'),
    path('courses/<int:course_id>/materials/', views.course_material_list, name='course-material-list'),
    path('courses/<int:course_id>/materials/<int:material_id>/', views.course_material_detail, name='course-material-detail'),
    path('sections/', views.section_list, name='section-list'),
    path('sections/<int:section_id>/', views.section_detail, name='section-detail'),
    path('quizzes/', views.quiz_list, name='quiz-list'),
    path('quizzes/<int:quiz_id>/', views.quiz_detail, name='quiz-detail'),
    path('quizzes/<int:quiz_id>/questions/', views.question_list, name='question-list'),
    path('quizzes/<int:quiz_id>/questions/<int:question_id>/', views.question_detail, name='question-detail'),
    path('submit-quiz-response/', views.submit_quiz_response, name='submit-quiz-response'),
    path('support-tickets/', views.support_ticket_view, name='support-ticket'),
    path('schedules/', views.schedule_view, name='schedule'),
    path('completed-courses/', views.completed_courses, name='completed-courses'),
    path('tutors/', views.list_and_create_tutors, name='list-create-tutors'),
    path('user/progress/', views.list_user_progress, name='user-progress'),
    path('user/update-progress/', views.update_course_progress, name='update-progress'),
]