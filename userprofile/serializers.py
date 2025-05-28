from rest_framework import serializers
from .models import Profile 
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =  fields = '__all__'  # Include other fields as needed

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
