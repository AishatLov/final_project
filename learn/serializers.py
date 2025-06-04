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
    SupportTicket,
    Schedule,
    CompletedCourse,
    CourseProgress,
    Section,
    CourseMaterial
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
        fields = ['id', 'user', 'profile_picture', 'bio', 'courses', 'availability']

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
        
class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = '__all__'

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
        
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'course', 'date', 'start_time', 'end_time']
        
    

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['id', 'user', 'subject', 'message', 'created_at', 'is_resolved']

class CompletedCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedCourse
        fields = ['id', 'user', 'course_id', 'completion_date', 'score']
        
class CourseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProgress
        fields = ['id', 'user', 'course', 'completion_status', 'score', 'last_accessed']
        
# serializer for section
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
    