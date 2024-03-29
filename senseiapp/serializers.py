from rest_framework import serializers
from .models import Teacher, Student, User, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'imageURL', 'bio', 'whatsapp_number', 'location', 'is_teacher']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = ['user', 'which_class']
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    student_list = StudentSerializer(many=True, read_only=True)
    class Meta:
        model = Teacher
        fields = ['user', 'qualifications', 'areas_of_expertise', 'student_list']
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user( **user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher


class ReviewSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    teacher = TeacherSerializer()

    class Meta:
        model = Review
        fields = ['id','teacher', 'student', 'content', 'rating']


