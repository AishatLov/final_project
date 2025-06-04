from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LearningPlan, OngoingCourse, CourseReward, Course, Quiz, SelectedQuizQuestion, Question, SupportTicket
from .serializers import (
    CourseResourceSerializer, 
    CourseSerializer, 
    LearningPlanSerializer, 
    OngoingCourseSerializer, 
    CourseRewardSerializer,
    QuizSerializer,
    SelectedQuizQuestionSerializer,
    QuestionSerializer,
    SupportTicketSerializer
)
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

class CourseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseResourceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CourseResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# New views for quiz functionality
class QuizListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

class SubmitQuizResponseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SelectedQuizQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SupportTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = SupportTicket.objects.filter(user=request.user)
        serializer = SupportTicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SupportTicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)