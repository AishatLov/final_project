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
    SelectedQuizQuestion,
    SupportTicket,
    Schedule,
    CompletedCourse,
    CourseProgress,
    Section,
    CourseMaterial,
)

# Register your models
admin.site.register(LearningPlan)
admin.site.register(OngoingCourse)
admin.site.register(CourseReward)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(CourseResource)

# Custom admin for CourseMaterial
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'uploaded_at']
    search_fields = ['title', 'course__name']
    list_filter = ['course']

admin.site.register(CourseMaterial, CourseMaterialAdmin)  # Register CourseMaterial with custom admin

# Registering new quiz-related models
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(SelectedQuizQuestion)

admin.site.register(SupportTicket)
admin.site.register(Schedule)
admin.site.register(CompletedCourse)
admin.site.register(Section)

# Register the Tutor model first
admin.site.register(Tutor)  # Register it before unregistering

# Custom admin for Tutor
class TutorAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_picture', 'bio']
    search_fields = ['user__username', 'bio']
    list_filter = ['courses'] 

# Unregister the default Tutor admin and register the custom one
admin.site.unregister(Tutor)
admin.site.register(Tutor, TutorAdmin)

class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'completion_status', 'score', 'last_accessed']
    search_fields = ['user__username', 'course__title']

admin.site.register(CourseProgress, CourseProgressAdmin)