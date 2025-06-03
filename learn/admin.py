from django.contrib import admin
from .models import (
    LearningPlan, 
    OngoingCourse, 
    CourseReward, 
    Course, 
    Tutor, 
    Category, 
    CourseResource,
    Quiz,
    Question,
    SelectedQuizQuestion
)

# Register your models
admin.site.register(LearningPlan)
admin.site.register(OngoingCourse)
admin.site.register(CourseReward)
admin.site.register(Course)
admin.site.register(Tutor)
admin.site.register(Category)
admin.site.register(CourseResource)

# Registering new quiz-related models
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(SelectedQuizQuestion)