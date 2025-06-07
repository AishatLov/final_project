from rest_framework import serializers
from .models import (
    Category,
    CourseReward, 
    Course, 
    Tutor, 
    CourseResource,
    Quiz,
    Question,
    Section,
    UserCourse,
    UserCourseReward,
    UserQuizResult
)

class TutorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Tutor
        fields = ['id', 'user', 'profile_picture', 'bio']

    def get_user(self,obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url  # fallback to relative URL
        return None
        
class CourseResourceSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = CourseResource
        fields = ['id', 'file', 'resource_type', 'resource_description', 
                 'resource_title', 'uploaded_at']
        
    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url  # fallback to relative URL
        return None
    
    # def get_file(self,obj):
    #     try:
    #         return obj.file.url
    #     except:
    #         return None

# New code start

class CategorySerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['name',"picture","id"]

    def get_picture(self, obj):
        request = self.context.get('request')
        if obj.picture and hasattr(obj.picture, 'url'):
            if request:
                return request.build_absolute_uri(obj.picture.url)
            return obj.picture.url  # fallback to relative URL
        return None

class BaseCourseSerializer(serializers.ModelSerializer):
    tutor = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "name",
            "description",
            "tutor",
            "category",
            "picture",
            "price",
            "rating",
            "student_count"
        ]

    def get_category(self,obj):
        return CategorySerializer(obj.category).data
    
    def get_tutor(self,obj):
        return TutorSerializer(obj.tutor).data
    
    def get_picture(self,obj):
        try:
            return obj.picture.url
        except:
            return None
        
class EnrolledCourseSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = UserCourse
        fields = ["course","id","date_started","completed","progress"]

    def get_progress(self,obj):
        count = 0
        completed_sections = obj.completed.split(",")
        for i in completed_sections:
            if len(i.strip()) > 0:
                count += 1
        all_section = Section.objects.filter(course=obj.course).count()

        try:
            percentage = (count * 100)/all_section
            print(percentage, " my percentage ", all_section, " ", count)
        except:
            return 0
        
        return round(percentage)

    def get_course(self,obj):
        return BaseCourseSerializer(obj.course).data


class CourseSectionResourceSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = CourseResource
        fields = ["resource_title","resource_type","resource_description","duration","id","file"]

    def get_file(Self,obj):
        try:
            return obj.file.url
        except:
            return None

class CourseSectionSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ["title","description","modules","id"]

    def get_modules(self,obj):
        resources = obj.resources.all()
        return CourseSectionResourceSerializer(resources, many=True).data
    
class CourseRewardSerializer(serializers.SerializerMethodField):
    picture = serializers.SerializerMethodField()

    class Meta:
        model = CourseReward
        fields = ['picture','title',"reward_description"]

    def get_picture(self,obj):
        try:
            return obj.picture.url
        except:
            return None
    
class UserCourseRewardSerializer(serializers.ModelSerializer):
    reward = serializers.SerializerMethodField()
    class Meta:
        model = UserCourseReward
        fields = ["reward","date_earned","id"]

    def get_reward(self,obj):
        return CourseRewardSerializer(obj.reward).data

class QuizMainSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ["title","id","completed"]

    def get_completed(self,obj):
        user = self.context.get("user",None)
        if user is None:
            return False
        try:
            UserQuizResult.objects.get(quiz=obj)
            return True
        except UserQuizResult.DoesNotExist:
            return False
        
class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class QuizDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    class Meta:
        model = Quiz
        fields = ["id","title","questions"]

    def get_questions(self,obj):
        questions = obj.questions.all()
        return QuizQuestionSerializer(questions, many=True).data
    
# New code End