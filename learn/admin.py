from django.contrib import admin
from .models import LearningPlan, OngoingCourse, CourseReward, Course

# Register your models
admin.site.register(LearningPlan)
admin.site.register(OngoingCourse)
admin.site.register(CourseReward)
admin.site.register(Course)