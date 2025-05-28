from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    file = models.FileField(upload_to='courses/', null=True, blank=True)

class LearningPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)  # Use ManyToManyField for courses

class OngoingCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255, default='Unnamed Course')  # Set a default value
    progress = models.FloatField(default=0.0)

class CourseReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward_description = models.TextField()