from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    LearningPlan, OngoingCourse, CourseReward, Course, Quiz,
    SelectedQuizQuestion, Question, SupportTicket, Schedule,
    CompletedCourse, Tutor, CourseResource, CourseProgress,
    Section, CourseMaterial
)
from .serializers import (
    CourseResourceSerializer, CourseSerializer, LearningPlanSerializer,
    OngoingCourseSerializer, CourseRewardSerializer, QuizSerializer,
    SelectedQuizQuestionSerializer, QuestionSerializer, SupportTicketSerializer,
    ScheduleSerializer, CompletedCourseSerializer, TutorSerializer,
    CourseProgressSerializer, SectionSerializer, CourseMaterialSerializer
)

# User Learning Plan View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_learning_plans(request):
    learning_plans = LearningPlan.objects.filter(user=request.user)
    serializer = LearningPlanSerializer(learning_plans, many=True)
    return Response(serializer.data if learning_plans.exists() else {"message": "No learning plans found."}, status=404 if not learning_plans.exists() else status.HTTP_200_OK)

# User Ongoing Courses View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_ongoing_courses(request):
    ongoing_courses = OngoingCourse.objects.filter(user=request.user)
    serializer = OngoingCourseSerializer(ongoing_courses, many=True)
    return Response(serializer.data)

# Upcoming Courses View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upcoming_courses(request):
    upcoming = Schedule.objects.filter()
    serializer = ScheduleSerializer(upcoming, many=True)
    return Response(serializer.data)

# User Course Rewards View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_course_rewards(request):
    course_rewards = CourseReward.objects.filter(user=request.user)
    serializer = CourseRewardSerializer(course_rewards, many=True)
    return Response(serializer.data)

# Download Center
def download_center(request):
    courses = Course.objects.all()
    return render(request, 'download_center.html', {'courses': courses})

# Course List View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Course Detail View
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def course_detail(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"message": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Course Material Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def course_material_list(request, course_id):
    if request.method == 'GET':
        materials = CourseMaterial.objects.filter(course_id=course_id)
        serializer = CourseMaterialSerializer(materials, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CourseMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course_id=course_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def course_material_detail(request, course_id, material_id):
    try:
        material = CourseMaterial.objects.get(id=material_id, course_id=course_id)
    except CourseMaterial.DoesNotExist:
        return Response({"message": "Material not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseMaterialSerializer(material)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CourseMaterialSerializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Section Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def section_list(request):
    if request.method == 'GET':
        sections = Section.objects.all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def section_detail(request, section_id):
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        return Response({"message": "Section not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SectionSerializer(section)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SectionSerializer(section, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Course Resource View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course_resource(request):
    serializer = CourseResourceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Quiz Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def quiz_list(request):
    if request.method == 'GET':
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def quiz_detail(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response({"message": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Question Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def question_list(request, quiz_id):
    if request.method == 'GET':
        questions = Question.objects.filter(quiz_id=quiz_id)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(quiz_id=quiz_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def question_detail(request, quiz_id, question_id):
    try:
        question = Question.objects.get(id=question_id, quiz_id=quiz_id)
    except Question.DoesNotExist:
        return Response({"message": "Question not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Submit Quiz Response View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz_response(request):
    serializer = SelectedQuizQuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Support Ticket View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def support_ticket_view(request):
    if request.method == 'GET':
        tickets = SupportTicket.objects.filter(user=request.user)
        serializer = SupportTicketSerializer(tickets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SupportTicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Schedule View
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def schedule_view(request):
    if request.method == 'GET':
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Completed Courses
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def completed_courses(request):
    completed_courses = CompletedCourse.objects.filter(user=request.user)
    serializer = CompletedCourseSerializer(completed_courses, many=True)
    return Response(serializer.data)

# Manage Tutors
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_and_create_tutors(request):
    if request.method == 'GET':
        # Optional filtering by course or availability
        course_id = request.query_params.get('course_id')
        if course_id:
            tutors = Tutor.objects.filter(courses__id=course_id).distinct()
        else:
            tutors = Tutor.objects.all()
        
        serializer = TutorSerializer(tutors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Progress
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_progress(request):  
    user_progress = CourseProgress.objects.filter(user=request.user)
    serializer = CourseProgressSerializer(user_progress, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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

# Course Material Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def course_material_list(request, course_id):
    if request.method == 'GET':
        materials = CourseMaterial.objects.filter(course_id=course_id)
        serializer = CourseMaterialSerializer(materials, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CourseMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course_id=course_id)  # Set the course association
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def course_material_detail(request, course_id, material_id):
    try:
        material = CourseMaterial.objects.get(id=material_id, course_id=course_id)
    except CourseMaterial.DoesNotExist:
        return Response({"message": "Material not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseMaterialSerializer(material)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CourseMaterialSerializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)