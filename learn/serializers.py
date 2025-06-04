from rest_framework import serializers
from .models import (
    LearningPlan, 
    OngoingCourse, 
    CourseReward, 
    Course, 
    Tutor, 
    CourseResource,
    Quiz,
    Question,
    SelectedQuizQuestion,
    SupportTicket
    
)

class LearningPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPlan
        fields = '__all__'

class OngoingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OngoingCourse
        fields = '__all__'

class CourseRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReward
        fields = '__all__'

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['id', 'user', 'profile_picture', 'bio']

class CourseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResource
        fields = ['id', 'course', 'file', 'resource_type', 'resource_description', 
                 'resource_title', 'uploaded_at']

class CourseSerializer(serializers.ModelSerializer):
    resources = CourseResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'duration', 'tutor', 'image', 
                 'created_at', 'resources']

# New serializers for Quiz functionality
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'description']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions', 'score']

class SelectedQuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedQuizQuestion
        fields = ['quiz', 'question', 'user_response']
        
    

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['id', 'user', 'subject', 'message', 'created_at', 'is_resolved']