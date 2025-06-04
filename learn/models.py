from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#from .models import Course  # Assuming Course model is in the same app

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(upload_to='tutors/')
    bio = models.TextField(blank=True)
    courses = models.ManyToManyField('Course', related_name='tutors', blank=True)  # Assuming a Course model exists
    availability = models.JSONField(default=dict)  # Store availability as JSON

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
    

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, related_name='materials', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_materials/')  # For file uploads
    link = models.URLField(blank=True, null=True)  # Optional link field
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

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
    
class CourseReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward_description = models.TextField()
    
# models for completing courses
class CompletedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.CharField(max_length=100)
    completion_date = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return "{} completed {} on {}".format(self.user.username, self.course_id, self.completion_date)

# course progress tracking  
class CourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completion_status = models.BooleanField(default=False) 
    score = models.FloatField(null=True, blank=True)  
    last_accessed = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = ('user', 'course')  # Ensure one progress record per user and course

    def __str__(self):
        return self.user.username + " - " + self.course.name + " Progress"
    
# models for learning plans and ongoing courses
class LearningPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course) 
    start_date = models.DateField() 
    end_date = models.DateField() 
    sessions = models.TextField() 

    def __str__(self):
        return self.user.username + "'s Learning Plan"

class OngoingCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255, default='Unnamed Course')  # Set a default value
    progress = models.FloatField(default=0.0)

# models for Quiz functionality
class Question(models.Model):
    description = models.CharField(max_length=255)
    options = models.JSONField(default=True)  # Store options as JSON for flexibility
    correct_answer = models.CharField(max_length=255, default=False)  # The correct answer

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
    
class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

# models for scheduling courses
class Schedule(models.Model):
    course = models.ForeignKey(Course, related_name='schedules', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return self.course.name + " - " + str(self.date) + " " + str(self.start_time) + " to " + str(self.end_time)
    
# models for section management
class Section(models.Model):
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField()  # To define the order of sections

    def __str__(self):
        return self.title
