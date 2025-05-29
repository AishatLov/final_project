from django.contrib import admin
from .models import LearningPlan, OngoingCourse, CourseReward, Course, Tutor, Category, CourseResource

# Register your models
admin.site.register(LearningPlan)
admin.site.register(OngoingCourse)
admin.site.register(CourseReward)
admin.site.register(Course)
admin.site.register(Tutor)
admin.site.register(Category)
admin.site.register(CourseResource)