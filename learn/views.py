from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LearningPlan, OngoingCourse, CourseReward, Course, Quiz, SelectedQuizQuestion, Question, SupportTicket, Schedule, CompletedCourse, Tutor, CourseResource, CourseProgress, Section, CourseMaterial
from .serializers import (
    CourseResourceSerializer, 
    CourseSerializer, 
    LearningPlanSerializer, 
    OngoingCourseSerializer, 
    CourseRewardSerializer,
    QuizSerializer,
    SelectedQuizQuestionSerializer,
    QuestionSerializer,
    SupportTicketSerializer,
    ScheduleSerializer,
    CompletedCourseSerializer,
    TutorSerializer,
    CourseProgressSerializer,
    SectionSerializer,
    CourseMaterialSerializer
)

class UserLearningPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        learning_plans = LearningPlan.objects.filter(user=user)
        serializer = LearningPlanSerializer(learning_plans, many=True)
        
        # Check if the user has any learning plans
        if learning_plans.exists():
            return Response(serializer.data)
        else:
            return Response({"message": "No learning plans found."}, status=404)

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
    
class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response({"message": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            serializer = CourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({"message": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({"message": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

# Course Material Views
class CourseMaterialListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        materials = CourseMaterial.objects.filter(course_id=course_id)
        serializer = CourseMaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request, course_id):
        serializer = CourseMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course_id=course_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseMaterialDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id, material_id):
        try:
            material = CourseMaterial.objects.get(id=material_id, course_id=course_id)
            serializer = CourseMaterialSerializer(material)
            return Response(serializer.data)
        except CourseMaterial.DoesNotExist:
            return Response({"message": "Material not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, course_id, material_id):
        try:
            material = CourseMaterial.objects.get(id=material_id, course_id=course_id)
            serializer = CourseMaterialSerializer(material, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CourseMaterial.DoesNotExist:
            return Response({"message": "Material not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, course_id, material_id):
        try:
            material = CourseMaterial.objects.get(id=material_id, course_id=course_id)
            material.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CourseMaterial.DoesNotExist:
            return Response({"message": "Material not found."}, status=status.HTTP_404_NOT_FOUND)

# section views
class SectionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sections = Section.objects.all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SectionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)
            serializer = SectionSerializer(section)
            return Response(serializer.data)
        except Section.DoesNotExist:
            return Response({"message": "Section not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)
            serializer = SectionSerializer(section, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Section.DoesNotExist:
            return Response({"message": "Section not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)
            section.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Section.DoesNotExist:
            return Response({"message": "Section not found."}, status=status.HTTP_404_NOT_FOUND)

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
    
# Schedule view for managing course schedules
class ScheduleView(APIView):
    def get(self, request):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# views for completing courses
@api_view(['GET'])
def completed_courses(request):
    completed_courses = CompletedCourse.objects.filter(user=request.user)
    serializer = CompletedCourseSerializer(completed_courses, many=True)
    return Response(serializer.data)

# views for managing tutors
@api_view(['GET'])
def list_tutors(request):
    tutors = Tutor.objects.all()
    serializer = TutorSerializer(tutors, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_tutor(request):
    serializer = TutorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_user_progress(request):
    user_progress = CourseProgress.objects.filter(user=request.user)
    serializer = CourseProgressSerializer(user_progress, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def update_course_progress(request):
    course_id = request.data.get('course_id')
    score = request.data.get('score')
    completion_status = request.data.get('completion_status')

    progress, created = CourseProgress.objects.update_or_create(
        user=request.user,
        course_id=course_id,
        defaults={'score': score, 'completion_status': completion_status}
    )

    return Response({"status": "success", "created": created})