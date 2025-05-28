from rest_framework import serializers
from .models import LearningPlan, OngoingCourse, CourseReward, Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

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