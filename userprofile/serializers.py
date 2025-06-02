from rest_framework import serializers
from .models import Profile, Topic, OnboardingQuestion
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields =  fields = '__all__'  # Include other fields as needed

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']  # Corrected indentation

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name']


class UserRegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        # Create token for the user
        Token.objects.create(user=user)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.username')
    topic_of_interest = TopicSerializer(many=True)
    
    class Meta:
            model = Profile
            fields = ['id' , 'user' , 'topic_of_interest']
  
   
class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['picture']   

class OnboardingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingQuestion
        fields = '__all__'