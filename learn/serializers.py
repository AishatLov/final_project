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

class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    resources = CourseResourceSerializer(many=True, read_only=True)
    materials = CourseMaterialSerializer(many=True, read_only=True)  # Adding materials

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'duration',
            'tutor',
            'image',
            'created_at',
            'resources',
            'materials'  # Including materials in the serialized output     
        ]
# New serializers for Quiz functionality
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'description', 'options', 'correct_answer']  # Include new fields

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)  # Nested serializer for related questions

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions', 'score']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)
        for question_data in questions_data:
            question = Question.objects.create(**question_data)
            quiz.questions.add(question)
        return quiz

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions')
        instance.title = validated_data.get('title', instance.title)
        instance.score = validated_data.get('score', instance.score)
        instance.save()

        # Update questions
        for question_data in questions_data:
            question_id = question_data.get('id')
            if question_id:
                question = Question.objects.get(id=question_id)
                question.description = question_data.get('description', question.description)
                question.options = question_data.get('options', question.options)
                question.correct_answer = question_data.get('correct_answer', question.correct_answer)
                question.save()
            else:
                # Create new question if no ID is provided
                Question.objects.create(quiz=instance, **question_data)
        return instance

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
    