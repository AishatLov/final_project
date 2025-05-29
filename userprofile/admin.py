from django.contrib import admin
from .models import Profile, Question, QuestionOption, UserQuestionResponse, Topic

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'internet_type', 'learning_type')
    search_fields = ('user__username', 'internet_type', 'learning_type')
    list_filter = ('internet_type', 'learning_type')


class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'description')
    search_fields = ('description',)
    list_filter = ('question',)

class UserQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'response')
    search_fields = ('user__username', 'question__description', 'response')
    list_filter = ('user', 'question')

# Register all models with their respective admin classes
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Question)
admin.site.register(QuestionOption, QuestionOptionAdmin)
admin.site.register(UserQuestionResponse, UserQuestionResponseAdmin)

admin.site.register(Topic)