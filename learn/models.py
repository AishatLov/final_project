from django.db import models
from django.contrib.auth.models import User

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(upload_to='tutors/')
    bio = models.TextField(blank=True)

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

    def __str__(self):
        return self.name

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
        return self.resource_title + " - " + self.course.name

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

# New models for Quiz functionality
class Question(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question, related_name='quizzes')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class SelectedQuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='selected_questions', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='selected_questions', on_delete=models.CASCADE)
    user_response = models.CharField(max_length=255)

    def __str__(self):
        return self.question.description + " - " + self.quiz.title
