from django.contrib import admin
from .models import Profile, Question, QuestionOption, UserQuestionResponse, Topic, OnboardingQuestion

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'internet_type', 'learning_type')
    search_fields = ('user__username', 'internet_type', 'learning_type')
    list_filter = ('internet_type', 'learning_type')

class UserQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'response')
    search_fields = ('user__username', 'question__description', 'response')
    list_filter = ('user', 'question')

class OnboardingQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'created_at')
    search_fields = ('question__text',)

# Register all models with their respective admin classes
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(UserQuestionResponse, UserQuestionResponseAdmin)

admin.site.register(Topic)
admin.site.register(OnboardingQuestion, OnboardingQuestionAdmin)
# Register other models as needed

class OnboardingQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'created_at')
    search_fields = ('question_text',)
