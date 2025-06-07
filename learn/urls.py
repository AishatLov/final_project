from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("quiz",views.ManageQuiz, basename="quiz")

urlpatterns = [
    path("category",views.ManageCourseCategory.as_view(), name="category"),
    path("tutor", views.ManageTutor.as_view(), name="tutor"),
    path("course", views.ManageCourse.as_view(), name="course"),
    path("course-resource/<int:id>",views.ManageCourseResource, name="course_resource"),
    path('course-rewards',views.ManageCourseReward, name="course_reward"),
    path("course-section/<int:id>", views.ManageCourseSection, name="course_section"),
    path("complete-section", views.markSectionsDone, name="complete_section"),
] + router.urls