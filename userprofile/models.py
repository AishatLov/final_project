from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    AGE_GROUP_CHOICES = [
        ('<15', 'Less than 15'),
        ('16-20', '16-20'),
        ('21-25', '21-25'),
        ('26-30', '26-30'),
        ('30+', '30+'),
    ]

    INTERNET_TYPE_CHOICES = [
        ('mobile_data', 'Mobile Data'),
        ('wifi', 'WiFi'),
        ('shared_device', 'Shared Device'),
    ]

    LEARNING_TYPE_CHOICES = [
        ('videos', 'Videos'),
        ('images', 'Images'),
        ('text_and_images', 'Text and Images'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES, default='<15')
    internet_type = models.CharField(max_length=20, choices=INTERNET_TYPE_CHOICES)
    learning_type = models.CharField(max_length=20, choices=LEARNING_TYPE_CHOICES)
    picture = models.FileField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Survey(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class UserQuestionResponse(models.Model):
    user = models.ForeignKey(User, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='responses', on_delete=models.CASCADE)
    response = models.CharField(max_length=255)

    def __str__(self):
         return self.response
   