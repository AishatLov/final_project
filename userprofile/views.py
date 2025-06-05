from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Profile, Question, Topic, UserQuestionResponse
from .serializers import ProfileSerializer, QuestionSerializer, UserRegistrationSerializer, TopicSerializer, OnboardingQuestionSerializer
from rest_framework.generics import ListCreateAPIView

class TopicView(ListCreateAPIView):
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

class GetOnboardingQuestions(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


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

    
