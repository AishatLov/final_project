from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Profile, Topic, OnboardingQuestion
from .serializers import ProfileSerializer, UserRegistrationSerializer, TopicSerializer, OnboardingQuestionSerializer


class TopicView(APIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

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
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class SetupProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        

# PENDING TASKS

class GetOnboardingQuestions(APIView):
    def get(self, request, format=None):
        questions = OnboardingQuestion.objects.all()
        serializer = OnboardingQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        """
        return all of the onboarding questions in our database
        1) get all questions
        2) serialized questions
        3) return questions
        """

class SaveUserQuestionResponse(APIView):
    def post(self,request,format=None):
        data = request.POST
        id = int(data['id'])
        response = data['answer']

        """
        1) use the id to get the question the user is answering

        question = Question.objects.get(id=id)
        try:
            formerResponse = UserQuestionResponse.objects.get(question=question)
            formerResponse.delete()
        except UserQuestionResponse.DoesNotExist:
            pass
            
        # create a new instance of UserQuestionResponse
        # set instance question 
        # set instance response
        # save instance

        2) return a Response
        """

    
