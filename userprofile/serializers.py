from rest_framework import serializers
from .models import Profile, Topic, OnboardingQuestion, Question, QuestionOption
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



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
        fields = ['name',"id"]


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

    topic_of_interest = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'age_group', 'internet_type',
            'learning_type', 'picture', 'topic_of_interest',
        ]

    def get_topic_of_interest(self,obj):
        return TopicSerializer(obj.topic_of_interest.all(),many=True).data

    def create(self, validated_data):
        topic_ids_str = validated_data.pop('topic_ids', '')
        topic_ids = [int(t.strip()) for t in topic_ids_str.split(',')]
        
        user = self.context['request'].user
        profile = Profile.objects.create(user=user, **validated_data)

        return profile

    
class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['picture']   

class OnboardingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingQuestion
        fields = '__all__'


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ["id","choice"]

class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ["description","options","id"]

    def get_options(self, obj):
        options = QuestionOption.objects.filter(question=obj)
        print(options)
        return QuestionOptionSerializer(options, many=True).data
