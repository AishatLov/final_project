from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Profile, Question, Topic, UserQuestionResponse
from .serializers import ProfileSerializer, QuestionSerializer, UserRegistrationSerializer, TopicSerializer, OnboardingQuestionSerializer
from rest_framework.generics import ListCreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

@extend_schema(
    summary="Get user info",
    description="Retrieve the authenticated user's info and XP.",
    tags=["User"],
    responses={
        200: OpenApiResponse(
            description="User info",
            examples=[
                OpenApiExample(
                    'User Info Example',
                    value={
                        "name": "John Doe",
                        "email": "john@example.com",
                        "xp": 120
                    }
                )
            ]
        )
    }
)

class UserInfo(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        user = request.user

        try:
            profile = Profile.objects.get(user=user)
            xp = profile.xp
        except Profile.DoesNotExist:
            xp =0
        # return a response wih the user information
        return Response({
            "first_name":user.first_name,
            "last_name":user.last_name,
            "email":user.email,
            "xp":xp
        },status=status.HTTP_200_OK)

@extend_schema(
    summary="List and create topics",
    description="Get all topics or create a new topic.",
    tags=["Topic"],
    responses={
        200: OpenApiResponse(
            response=TopicSerializer(many=True),
            description="List of topics",
            examples=[
                OpenApiExample(
                    'Topic List Example',
                    value=[
                        {"id": 1, "name": "Math"},
                        {"id": 2, "name": "Science"}
                    ]
                )
            ]
        ),
        201: OpenApiResponse(
            response=TopicSerializer,
            description="Created topic",
            examples=[
                OpenApiExample(
                    'Topic Created Example',
                    value={"id": 3, "name": "English"}
                )
            ]
        )
    }
)
class TopicView(ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

@extend_schema(
    summary="Get or update user profile",
    description="Retrieve or update the authenticated user's profile.",
    tags=["Profile"],
    responses={
        200: OpenApiResponse(
            response=ProfileSerializer,
            description="User profile",
            examples=[
                OpenApiExample(
                    'Profile Example',
                    value={
                        "id": 1,
                        "age_group": "16-20",
                        "internet_type": "wifi",
                        "learning_type": "videos",
                        "picture": "/media/profile_pictures/john.png",
                        "topic_of_interest": [
                            {"id": 1, "name": "Math"},
                            {"id": 2, "name": "Science"}
                        ]
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Invalid data", examples=[OpenApiExample('Error', value={"error": "Invalid data"})])
    }
)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema(
    summary="User login",
    description="Authenticate user and return token.",
    tags=["Auth"],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'password': {'type': 'string'}
            }
        }
    },
    responses={
        200: OpenApiResponse(description="Login successful", examples=[OpenApiExample('Token', value={"token": "abc123token"})]),
        400: OpenApiResponse(description="Invalid credentials", examples=[OpenApiExample('Error', value={"error": "Invalid credentials"})])
    }
)
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Setup or update user profile",
    description="Setup or update the authenticated user's profile, including topics of interest.",
    tags=["Profile"],
    request={
        'application/x-www-form-urlencoded': {
            'type': 'object',
            'properties': {
                'age_group': {'type': 'string'},
                'internet_type': {'type': 'string'},
                'learning_type': {'type': 'string'},
                'picture': {'type': 'string', 'format': 'binary'},
                'topic_ids': {'type': 'string', 'description': 'Comma-separated topic IDs'}
            }
        }
    },
    responses={
        200: OpenApiResponse(
            response=ProfileSerializer,
            description="Profile updated",
            examples=[
                OpenApiExample(
                    'Profile Updated Example',
                    value={
                        "id": 1,
                        "age_group": "16-20",
                        "internet_type": "wifi",
                        "learning_type": "videos",
                        "picture": "/media/profile_pictures/john.png",
                        "topic_of_interest": [
                            {"id": 1, "name": "Math"},
                            {"id": 2, "name": "Science"}
                        ]
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Invalid data", examples=[OpenApiExample('Error', value={"error": "Invalid data"})])
    }
)
class SetupProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        data = request.POST

        if serializer.is_valid():
            profile = serializer.save()
            if "topic_ids" in data.keys():
                topics = [int(id) for id in data['topic_ids'].split(",")]
                selected_topics = Topic.objects.filter(id__in=topics)
                profile.topic_of_interest.set(selected_topics)
                profile.save()

            return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(
    summary="User registration",
    description="Register a new user and return token.",
    tags=["Auth"],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'email': {'type': 'string'},
                'password': {'type': 'string'},
                'first_name': {'type': 'string'},
                'last_name': {'type': 'string'}
            }
        }
    },
    responses={
        201: OpenApiResponse(description="Registration successful", examples=[OpenApiExample('Token', value={"token": "abc123token"})]),
        400: OpenApiResponse(description="Invalid data", examples=[OpenApiExample('Error', value={"error": "Invalid data"})])
    }
)
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Update profile picture",
    description="Update the authenticated user's profile picture.",
    tags=["Profile"],
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'picture': {'type': 'string', 'format': 'binary'}
            }
        }
    },
    responses={
        200: OpenApiResponse(description="Profile picture updated", examples=[OpenApiExample('Success', value={"message": "Profile picture updated"})]),
        400: OpenApiResponse(description="Profile not found", examples=[OpenApiExample('Error', value={})])
    }
)
class UpdateProfilePictureView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            picture = request.FILES.get('picture')

            profile.picture = picture
            profile.save()
            return Response({'message': 'Profile picture updated'}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        

@extend_schema(
    summary="List onboarding questions",
    description="Get all onboarding questions.",
    tags=["Onboarding"],
    responses={
        200: OpenApiResponse(
            response=QuestionSerializer(many=True),
            description="List of onboarding questions",
            examples=[
                OpenApiExample(
                    'Onboarding Questions Example',
                    value=[
                        {"id": 1, "description": "What is your favorite subject?", "options": [{"id": 1, "choice": "Math"}, {"id": 2, "choice": "Science"}]}
                    ]
                )
            ]
        )
    }
)
class GetOnboardingQuestions(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


@extend_schema(
    summary="Save user onboarding question response",
    description="Save a user's response to an onboarding question.",
    tags=["Onboarding"],
    request={
        'application/x-www-form-urlencoded': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'answer': {'type': 'string'}
            }
        }
    },
    responses={
        200: OpenApiResponse(description="Response saved", examples=[OpenApiExample('Saved', value={})]),
        400: OpenApiResponse(description="Invalid question", examples=[OpenApiExample('Error', value={})])
    }
)
class SaveUserQuestionResponse(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        data = request.POST
        id = int(data['id'])
        response = data['answer']

        try:
            question = Question.objects.get(id=id)
            try:
                formerResponse = UserQuestionResponse.objects.get(question=question)
                formerResponse.delete()
            except UserQuestionResponse.DoesNotExist:
                pass

            userresponse = UserQuestionResponse(
                question = question,
                user=request.user,
                response=response
            )

            userresponse.save()
            return Response({}, status=status.HTTP_200_OK)
        except Question.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


