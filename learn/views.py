from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LearningPlan, OngoingCourse, CourseReward, Course
from .serializers import LearningPlanSerializer, OngoingCourseSerializer, CourseRewardSerializer
from django.contrib.auth.models import User


class UserLearningPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        learning_plan = LearningPlan.objects.filter(user=user)
        serializer = LearningPlanSerializer(learning_plan, many=True)
        return Response(serializer.data)

class UserOngoingCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        ongoing_courses = OngoingCourse.objects.filter(user=user)
        serializer = OngoingCourseSerializer(ongoing_courses, many=True)
        return Response(serializer.data)

class UserCourseRewardsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        course_rewards = CourseReward.objects.filter(user=user)
        serializer = CourseRewardSerializer(course_rewards, many=True)
        return Response(serializer.data)
    

def download_center(request):
    courses = Course.objects.all()  # Fetch all courses
    return render(request, 'download_center.html', {'courses': courses})