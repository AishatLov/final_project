from django.db import models
from django.contrib.auth.models import User


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(upload_to='tutors/')
    bio = models.TextField(blank=True)
#   created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    picture = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class CourseResource(models.Model):
    Resource_types = (
        ('video', 'Video'),
        ('image', 'Image'),
        ('text', 'Text'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    file = models.FileField(upload_to='resources/')
    resource_type = models.CharField(max_length=10, choices=Resource_types)
    resource_description = models.TextField()
    resource_title = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource_title} - {self.course.name}"

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
    