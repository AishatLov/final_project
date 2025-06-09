from django.db.models import Q
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, extend_schema_view, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view

from userprofile.models import Profile

from .models import (
    Category, CourseReward, Course, Quiz,Tutor, Question,
    CourseResource,Section, UserCourse, UserCourseReward, UserQuizQuestionResponse, UserQuizResult
)

from .serializers import (
    BaseCourseSerializer, CategorySerializer, 
    CourseResourceSerializer, CourseSectionSerializer, 
    EnrolledCourseSerializer, QuizDetailSerializer, QuizMainSerializer, TutorSerializer, UserCourseRewardSerializer
)


"""
    - get tutor - done
    - enroll in course -- done
    - get course category -- done
    - get course (filter by category) -- done
    - get enrolled course (completed, ongoing, category) -- done

    - course details                             - done
    - course resources                           - done
    - mark section as complete (course progress) - done
 
    - top tutors -- done
    - popular courses -- done
    - filter course by start_date -- done

    - get user info -- done # add user xp to this -- done
    - get and set course reward (all, for course) -- done 


    - quiz -- done
        - get quiz questions -- done
        - save user reponse -- done
        - get user quiz assessment -- done

    - get learning schedule : TODO(pending)

    #might need to add date to course section, so user can filter by date
"""

@extend_schema_view(
    list=extend_schema(
        summary="List all quizzes",
        description="Get a list of all available quizzes",
        tags=["Quiz"],
        responses={
            200: OpenApiResponse(
                response=QuizMainSerializer(many=True),
                description="List of quizzes",
                examples=[
                    OpenApiExample(
                        'Quiz List Example',
                        value=[
                            {"id": 1, "title": "Sample Quiz", "completed": False},
                            {"id": 2, "title": "Another Quiz", "completed": True}
                        ]
                    )
                ]
            )
        }
    ),
    retrieve=extend_schema(
        summary="Get quiz details or results",
        description="Retrieve quiz questions or quiz result for a specific quiz",
        parameters=[
            OpenApiParameter(name="result", type=bool, location=OpenApiParameter.QUERY, description="Get quiz result instead of questions")
        ],
        tags=["Quiz"],
        responses={
            200: OpenApiResponse(
                response=QuizDetailSerializer,
                description="Quiz detail or result",
                examples=[
                    OpenApiExample(
                        'Quiz Detail Example',
                        value={
                            "id": 1,
                            "title": "Sample Quiz",
                            "questions": [
                                {"id": 1, "description": "What is 2+2?", "options": ["3", "4", "5"], "correct_answer": "4"}
                            ]
                        }
                    ),
                    OpenApiExample(
                        'Quiz Result Example',
                        value={"result": 80}
                    )
                ]
            ),
            400: OpenApiResponse(description="Quiz not found or user has not taken the quiz", examples=[OpenApiExample('Error', value={"msg": "user has taken thi quiz"})])
        }
    ),
    create=extend_schema(
        summary="Submit quiz answer",
        description="Save user's response to quiz questions",
        request={
            'application/x-www-form-urlencoded': {
                'type': 'object',
                'properties': {
                    'quiz': {'type': 'integer'},
                    'question': {'type': 'integer'},
                    'answer': {'type': 'string'},
                    'last': {'type': 'boolean', 'required': False}
                }
            }
        },
        tags=["Quiz"],
        responses={
            200: OpenApiResponse(description="Quiz answer saved", examples=[OpenApiExample('Saved', value={})]),
            400: OpenApiResponse(description="Quiz does not exist", examples=[OpenApiExample('Error', value={"msg": "quiz does not exist"})]),
            201: OpenApiResponse(description="Quiz completed and result returned", examples=[OpenApiExample('Result', value={"result": 90})])
        }
    )
)
class ManageQuiz(ViewSet):
    def list(self, request):
        queryset = Quiz.objects.all()
        serializer = QuizMainSerializer(queryset, many=True, context={"user":request.user})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
            retrieve quiz questions or quiz result
        """
        result = request.query_params.get("result")

        quiz = Quiz.objects.get(id=pk)

        if result is not None and result == "true":
            # return quiz result
            try:
                result = UserQuizResult.objects.get(quiz=quiz)
                return Response({'result':result.score})
            except UserQuizResult.DoesNotExist:
                return Response({"msg":"user has not taken this quiz"},status=status.HTTP_400_BAD_REQUEST)
        else:
            #return quiz questions
            serializer = QuizDetailSerializer(quiz)
            return Response(serializer.data)
    
    def create(self, request):
        """ Save Individual quiz question response """
        data = request.POST
        quiz_id = int(data['quiz'])
        question_id = int(data['question'])
        answer = data['answer'].strip()

        try:
            quiz = Quiz.objects.get(id=quiz_id)
            question = Question.objects.get(id=question_id)

            try:
                res = UserQuizQuestionResponse.objects.get(Q(question=question)&Q(user=request.user))
                res.delete()
            except UserQuizQuestionResponse.DoesNotExist:
                pass

            response = UserQuizQuestionResponse(
                question = question,
                option_selected = answer,
                correct_option = question.correct_answer == answer,
                user = request.user
            )

            response.save()

            if "last" in data.keys() and data['last'] == "true":
                all_response = UserQuizQuestionResponse.objects.filter(question__in=quiz.questions.all())
                correct_resp = all_response.filter(correct_option=True).count()

                score = round((correct_resp * 100)/all_response.count())

                try:
                    result = UserQuizResult.objects.get(Q(quiz=quiz)&Q(user=request.user))
                    result.delete()
                except UserQuizResult.DoesNotExist:
                    pass

                result = UserQuizResult(
                    quiz = quiz,
                    score=score,
                    user=request.user
                )

                result.save()

                return Response({'result':result.score})
            return Response({})
        except Quiz.DoesNotExist:
            return Response({'msg':"quiz does not exist"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Get all categories",
    description="Get a list of all course categories",
    tags=["Categories"],
    responses={
        200: OpenApiResponse(
            response=CategorySerializer(many=True),
            description="List of categories",
            examples=[
                OpenApiExample(
                    'Category List Example',
                    value={
                        "categories": [
                            {"id": 1, "name": "Programming", "picture": "/media/cat1.png"},
                            {"id": 2, "name": "Math", "picture": "/media/cat2.png"}
                        ]
                    }
                )
            ]
        )
    }
)
class ManageCourseCategory(APIView):
    def get(self,request,format=None):
        category = Category.objects.all()

        return Response({'categories':CategorySerializer(category, many=True,context={'request': request}).data}, status=status.HTTP_200_OK)

@extend_schema(
    summary="Get all tutors",
    description="Get a list of all tutors ordered by rating",
    tags=["Tutors"],
    responses={
        200: OpenApiResponse(
            response=TutorSerializer(many=True),
            description="List of tutors",
            examples=[
                OpenApiExample(
                    'Tutor List Example',
                    value={
                        "tutors": [
                            {"id": 1, "user": "John Doe", "profile_picture": "/media/tutors/john.png", "bio": "Expert in Python."}
                        ]
                    }
                )
            ]
        )
    }
)
class ManageTutor(APIView):
    def get(self,request,format=None):
        tutors = Tutor.objects.all().order_by("rating")
        return Response({"tutors":TutorSerializer(tutors, many=True,context={'request': request}).data})

@extend_schema(
    summary="Get course sections",
    description="Get detailed information about course sections",
    tags=["Courses"],
    parameters=[OpenApiParameter(name="id", location=OpenApiParameter.PATH, type=int, description="Course ID")],
    responses={
        200: OpenApiResponse(
            response=CourseSectionSerializer(many=True),
            description="Course sections and details",
            examples=[
                OpenApiExample(
                    'Course Section Example',
                    value={
                        "course": {
                            "name": "Python 101",
                            "description": "Intro to Python",
                            "tutor": {"id": 1, "user": "John Doe", "profile_picture": "/media/tutors/john.png", "bio": "Expert in Python."},
                            "category": {"id": 1, "name": "Programming", "picture": "/media/cat1.png"},
                            "picture": "/media/courses/python.png",
                            "price": "0.00",
                            "rating": 5,
                            "student_count": 100
                        },
                        "sections": [
                            {"title": "Getting Started", "description": "Basics", "modules": [], "id": 1}
                        ]
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Course not found", examples=[OpenApiExample('Error', value={})])
    }
)
@api_view(['get'])
def ManageCourseSection(request,id):
    try:
        course = Course.objects.get(id=id)
        sections = Section.objects.filter(course=course).order_by("order")
        return Response({
            "course":BaseCourseSerializer(course).data,
            "sections":CourseSectionSerializer(sections, many=True).data
        })
    except Course.DoesNotExist:
        return Response({},status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Mark section as complete",
    description="Mark a course section as completed",
    tags=["Courses"],
    request={
        'application/x-www-form-urlencoded': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'}
            }
        }
    },
    responses={
        200: OpenApiResponse(
            response=UserCourseRewardSerializer(many=True),
            description="Section marked as complete, rewards returned if any",
            examples=[
                OpenApiExample(
                    'Section Complete Example',
                    value={
                        'rewards': [
                            {"id": 1, "reward": {"picture": "/media/reward.png", "title": "Beginner", "reward_description": "Completed first section."}, "date_earned": "2024-06-06T12:00:00Z"}
                        ]
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Section or course not found", examples=[OpenApiExample('Error', value={})])
    }
)
@api_view(['post'])
def markSectionsDone(request):
    data = request.POST
    id = int(data['id'])
    msg = "untouched"

    try:
        section = Section.objects.get(id=id)
        try:
            course = UserCourse.objects.get(Q(user=request.user)&Q(course=section.course))
            completed_sections = course.completed.split(",")

            if str(section.id) not in completed_sections:
                completed_sections.append(str(section.id))
                course.completed = ",".join(completed_sections)
                course.save()

                try:
                    profile = Profile.objects.get(user=request.user)
                    profile.xp += 10
                    profile.save()

                    prev_reward_ids = [reward.reward.id for reward in UserCourseReward.objects.filter(user=request.user)]
                    rewards = CourseReward.objects.filter(xp_target__lte=profile.xp).exclude(id__in=prev_reward_ids)

                    rewards_new = []
                    # set new rewards
                    for reward in rewards:
                        new_reward = UserCourseReward(reward=reward, user=request.user)
                        new_reward.save()
                        rewards_new.append(new_reward)

                    return Response({
                        'rewards':UserCourseRewardSerializer(rewards_new, many=True).data
                    },status=status.HTTP_200_OK)
                
                except Profile.DoesNotExist:
                    return Response({},status=status.HTTP_200_OK)
            else:
                return Response({"msg":"already marked as completed"})

        except UserCourse.DoesNotExist:
            msg = "no coursce"
            return Response({"msg":msg},status=status.HTTP_400_BAD_REQUEST)
            # pass

    except Section.DoesNotExist:
        msg = "section error"
        return Response({"msg":msg},status=status.HTTP_400_BAD_REQUEST)
        # pass
    
    

@extend_schema(
    summary="Get course resources",
    description="Get resources for a specific course",
    tags=["Courses"],
    parameters=[OpenApiParameter(name="id", location=OpenApiParameter.PATH, type=int, description="Course ID")],
    responses={
        200: OpenApiResponse(
            response=CourseResourceSerializer(many=True),
            description="Course resources",
            examples=[
                OpenApiExample(
                    'Course Resource Example',
                    value={
                        "modules": [
                            {"id": 1, "course": 1, "file": "/media/resources/vid.mp4", "resource_type": "video", "resource_description": "Intro video", "resource_title": "Introduction", "uploaded_at": "2024-06-06T12:00:00Z"}
                        ]
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Course not found", examples=[OpenApiExample('Error', value={})])
    }
)
@api_view(['get'])
def ManageCourseResource(request,id):
    try:
        course = Course.objects.get(id=id)
        sections = Section.objects.filter(course=course)
        resource_id = []

        for i in sections:
            ids = [x.id for x in i.resources.all()]
            resource_id.extend(ids)

        resources = CourseResource.objects.filter(id__in=resource_id)
        print(resources, " oya ooo")
        return Response({
            "modules":CourseResourceSerializer(resources, many=True,context={'request': request}).data,
        })
    
    except Course.DoesNotExist:
        return Response({},status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Get user rewards",
    description="Get all rewards earned by the user",
    tags=["Rewards"],
    responses={
        200: OpenApiResponse(
            response=UserCourseRewardSerializer(many=True),
            description="User rewards",
            examples=[
                OpenApiExample(
                    'User Rewards Example',
                    value={
                        'rewards': [
                            {"id": 1, "reward": {"picture": "/media/reward.png", "title": "Beginner", "reward_description": "Completed first section."}, "date_earned": "2024-06-06T12:00:00Z"}
                        ]
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="User not authenticated", examples=[OpenApiExample('Error', value={})])
    }
)
@api_view(['get'])
def ManageCourseReward(request):
    if request.user.is_anonymous:
        return Response({},status=status.HTTP_400_BAD_REQUEST)
    
    user_rewards = UserCourseReward.objects.filter(user=request.user)
    return Response({
        'rewards':UserCourseRewardSerializer(user_rewards, many=True).data
    })


@extend_schema_view(
    get=extend_schema(
        summary="List courses",
        description="Get courses with optional filters. PS : AUTHENTICATED REQUEST SHOULD INCLUDE THE AUTHORIZATION HEADER, completed and enrolled parameter need this header set",
        parameters=[
            OpenApiParameter(name="category", type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="completed", type=bool, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="enrolled", type=bool, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="date", type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="popular", type=bool, location=OpenApiParameter.QUERY)
        ],
        tags=["Courses"],
        responses={
            200: OpenApiResponse(
                response=BaseCourseSerializer(many=True),
                description="List of courses or enrolled courses",
                examples=[
                    OpenApiExample(
                        'Course List Example',
                        value={
                            "courses": [
                                {"name": "Python 101", "description": "Intro to Python", "tutor": {"id": 1, "user": "John Doe", "profile_picture": "/media/tutors/john.png", "bio": "Expert in Python."}, "category": {"id": 1, "name": "Programming", "picture": "/media/cat1.png"}, "picture": "/media/courses/python.png", "price": "0.00", "rating": 5, "student_count": 100}
                            ]
                        }
                    ),
                    OpenApiExample(
                        'Enrolled Course Example',
                        value={
                            "courses": [
                                {"course": {"name": "Python 101", "description": "Intro to Python", "tutor": {"id": 1, "user": "John Doe", "profile_picture": "/media/tutors/john.png", "bio": "Expert in Python."}, "category": {"id": 1, "name": "Programming", "picture": "/media/cat1.png"}, "picture": "/media/courses/python.png", "price": "0.00", "rating": 5, "student_count": 100}, "id": 1, "date_started": "2024-06-06T12:00:00Z", "completed": False, "progress": 50}
                            ]
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Authentication or course error", examples=[OpenApiExample('Error', value={"error": "you need to be logged in to see authenticated courser"})])
        }
    ),
    post=extend_schema(
        summary="Enroll in course",
        description="Enroll user in a specific course",
        request={
            'application/x-www-form-urlencoded': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'}
                }
            }
        },
        tags=["Courses"],
        responses={
            201: OpenApiResponse(description="Enrolled successfully", examples=[OpenApiExample('Enrolled', value={})]),
            400: OpenApiResponse(description="Enrollment error", examples=[OpenApiExample('Error', value={"error": "Course already enrolled"})])
        }
    )
)
class ManageCourse(APIView):
    def get(self,request,format=None):
        category = request.query_params.get("category")
        completed = request.query_params.get("completed")
        enrolled = request.query_params.get("enrolled")
        date = request.query_params.get("date")
        popular = request.query_params.get("popular")


        if enrolled is not None:
            if request.user.is_anonymous:
                return Response({
                    "error":"you need to be logged in to see authenticated courser"
                },status=status.HTTP_400_BAD_REQUEST)
            
            courses = UserCourse.objects.filter(user=request.user)

            if completed is not None:
                if completed.lower().strip() == "true":
                    courses = courses.filter(completed=completed.lower().strip() == "true")

            return Response({"courses":EnrolledCourseSerializer(courses, many=True).data})
        else:
            courses = Course.objects.all()
            if category is not None:
                try:
                    current_category = Category.objects.get(name=category.strip())
                    courses = courses.filter(category=current_category)
                except Category.DoesNotExist:
                    courses = []

            if date is not None:
                courses = courses.filter(start_date=date)

            if popular is not None:
                courses = courses.order_by("student_count")

            data = BaseCourseSerializer(courses, many=True).data
            print(data)
            
            return Response(data={"courses":data},status=status.HTTP_200_OK)
        
    def post(self,request,format=None):
        """ enroll course """
        data = request.POST
        id = data['id']

        if request.user.is_anonymous:
            error = "you need to be logged in to enroll course"
        else:
            try:
                course = Course.objects.get(id=id)
                user_course = UserCourse.objects.get(Q(user=request.user)&Q(course=course))
                error = "Course already enrolled"
            except UserCourse.DoesNotExist:
                course = Course.objects.get(id=id)
                user_course = UserCourse(
                    course = course,
                    user = request.user
                )
                user_course.save()

                return Response({},status=status.HTTP_201_CREATED)
            
            except Course.DoesNotExist:
                error = "No Course with the specified id"
            
        return Response({
                "error":error
            },status=status.HTTP_400_BAD_REQUEST)