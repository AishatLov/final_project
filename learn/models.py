from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(upload_to='tutors/')
    bio = models.TextField(blank=True)
    rating = models.PositiveIntegerField(default=1)

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
    picture = models.FileField(null=True,default=None, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    rating = models.PositiveIntegerField(default=1)
    student_count = models.PositiveIntegerField(default=0)
    start_date = models.DateField(null=True,blank=True,default=None)

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
    file = models.FileField(upload_to='resources/')
    resource_type = models.CharField(max_length=10, choices=Resource_types)
    resource_description = models.TextField()
    resource_title = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.resource_title 
    
class CourseReward(models.Model):
    picture = models.FileField(null=True,blank=True,default=None)
    title = models.CharField(max_length=100, default="")
    reward_description = models.TextField()
    xp_target = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


# models for Quiz functionality
class Question(models.Model):
    description = models.CharField(max_length=255)
    options = models.JSONField(default=list)  # Store options as JSON for flexibility
    correct_answer = models.CharField(max_length=255, default=False)  # The correct answer

    def __str__(self):
        return self.description

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question, related_name='quizzes')

    def __str__(self):
        return self.title
    
class UserQuizQuestionResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_selected = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_option = models.BooleanField(default=False)
    
class UserQuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# models for section management
class Section(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField(default=1) # order in which section are been displayed 
    resources = models.ManyToManyField(CourseResource, blank=True)
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# models for scheduling courses
class Schedule(models.Model):
    course = models.ForeignKey(Course, related_name='schedules', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return self.course.name + " - " + str(self.date) + " " + str(self.start_time) + " to " + str(self.end_time)
    
# New code
class UserCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_started = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    progress = models.PositiveIntegerField(default=0)
    completed = models.TextField(default="",blank=True)

    def __str__(self):
        return f"{self.user.email} {self.course.name}"
    

class UserCourseReward(models.Model):
    reward = models.ForeignKey(CourseReward, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reward.title
    

# models for learning plans and ongoing courses
class LearningPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course) 
    start_date = models.DateField() 
    end_date = models.DateField() 
    sessions = models.TextField() 

    def __str__(self):
        return self.user.username + "'s Learning Plan"

