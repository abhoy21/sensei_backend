from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Teacher, User, Student, Review
from .serializers import TeacherSerializer, StudentSerializer, UserSerializer, ReviewSerializer


class UserRegistration(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        is_teacher = request.data.get('is_teacher')
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')
        imageURL = request.data.get('imageURL', '')  # Providing default value if not present
        bio = request.data.get('bio')
        whatsapp_number = request.data.get('whatsapp_number')
        location = request.data.get('location')


        user_data = {
            'is_teacher': is_teacher,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'imageURL': imageURL,
            'bio': bio,
            'whatsapp_number': whatsapp_number,
            'location': location

        }
        #
        # serializer = self.serializer_class(data=user_data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.save()

        if is_teacher:
            qualifications = request.data.get('qualifications')
            areas_of_expertise = request.data.get('areas_of_expertise', [])

            teacher_data = {
                'user': user_data,
                'qualifications': qualifications,
                'areas_of_expertise': areas_of_expertise
            }

            teacher_serializer = TeacherSerializer(data=teacher_data)
            teacher_serializer.is_valid(raise_exception=True)
            teacher = teacher_serializer.save()
        else:
            which_class = request.data.get('which_class')
            student_data = {
                'user': user_data,
                'which_class': which_class
            }
            student_serializer = StudentSerializer(data=student_data)
            student_serializer.is_valid(raise_exception=True)
            student = student_serializer.save()
        if is_teacher:
            return Response(teacher_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(student_serializer.data, status=status.HTTP_201_CREATED)


class TeacherDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            teacher = Teacher.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Teacher.DoesNotExist:
            return Response({"message": "Teacher not found for this user"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)



class TeacherListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Teacher.objects.all()
        serializer = TeacherSerializer(queryset, many=True)

        return Response(serializer.data)



class IsTeacherAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            is_teacher = user.is_teacher
            return Response({'is_teacher': is_teacher})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class TeacherEditAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')  # Assuming 'username' is provided in request data
        if not username:
            return Response({"message": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(detail="User not found")

        # Check if the user is a teacher
        if not user.is_teacher:
            return Response({"message": "Only teachers can edit details"}, status=status.HTTP_403_FORBIDDEN)

        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({"message": "Teacher profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AddStudentToTeacher(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Get data from request
        teacher_id = request.data.get('id')
        student_username = request.data.get('username')

        # Check if teacher_id and student_username are provided
        if not teacher_id or not student_username:
            return Response({"error": "Teacher ID and Student Username are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if the teacher exists
        teacher = get_object_or_404(Teacher, pk=teacher_id)

        # Check if the teacher is actually a teacher
        if not teacher.user.is_teacher:
            return Response({"error": "Specified user is not a teacher."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if the student exists
        student_user = get_object_or_404(User, username=student_username)

        # Check if the student is actually a student
        try:
            student = student_user.student
        except Student.DoesNotExist:
            return Response({"error": "Specified user is not a student."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Add student to teacher's student list
        teacher.student_list.add(student)

        return Response({"success": "Student added to teacher's student list."},
                        status=status.HTTP_200_OK)


class StudentListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, teacher_username):
        # Retrieve the teacher object based on the provided username
        teacher_user = get_object_or_404(User, username=teacher_username)
        teacher = get_object_or_404(Teacher, user=teacher_user)

        # Check if the user is a teacher
        if not teacher_user.is_teacher:
            return JsonResponse({'error': 'User is not a teacher'}, status=400)

        # Get the list of students associated with the teacher
        student_list = teacher.student_list.all()

        # Construct the response data
        students_data = []
        for student in student_list:
            student_data = {
                'username': student.user.username,
                'first_name': student.user.first_name,
                'last_name': student.user.last_name,
                'class': student.which_class,
                # Add more fields as needed
            }
            students_data.append(student_data)

        return JsonResponse({'students': students_data})


class CheckUsernameInStudentListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        student_username = request.data.get('student_username', None)
        teacher_username = request.data.get('teacher_username', None)

        if not student_username or not teacher_username:
            return Response({"error": "Both student_username and teacher_username are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(user__username=teacher_username)
            student_list = teacher.student_list.all()
            if student_list.filter(user__username=student_username).exists():
                return Response({"result": True}, status=status.HTTP_200_OK)
            else:
                return Response({"result": False}, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher with this username does not exist"}, status=status.HTTP_404_NOT_FOUND)


class AddReview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        teacher_username = request.data.get('teacher_username')
        student_username = request.data.get('student_username')
        content = request.data.get('content')
        rating = request.data.get('rating')

        # Fetch teacher and student instances
        try:
            teacher = Teacher.objects.get(user__username=teacher_username)
            student = Student.objects.get(user__username=student_username)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create and save the review
        review = Review.objects.create(content=content, rating=rating, teacher=teacher, student=student)
        review.save()

        return Response({"success": "Review added successfully"}, status=status.HTTP_201_CREATED)


class TeacherReviewStudentsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        try:
            teacher = Teacher.objects.get(user__username=username)
            reviews = Review.objects.filter(teacher=teacher)
            students = []
            for review in reviews:
                if review.student:
                    students.append({
                        'student_username': review.student.user.username,
                        'student_first_name': review.student.user.first_name,
                        'student_last_name': review.student.user.last_name,
                        'review_content': review.content,
                        'review_rating': review.rating,
                        'imageURL': review.student.user.imageURL
                    })
            return Response(students, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)


class TeacherSearch(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query')  # Change request.data to request.query_params
        teachers = Teacher.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__location__icontains=query) |
            Q(qualifications__icontains=query) |
            Q(areas_of_expertise__contains=[query])
        )
        serializer = TeacherSerializer(teachers, many=True)  # Change serialize to serializer

        return Response(serializer.data)


class UserDetailView(APIView):
    def get(self, request):
        username = request.query_params.get('username', None)
        if username is None:
            return Response({'error': 'Username parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)

        if user.is_teacher:
            response_data = {
                'message': f'The user {username} is a teacher.',
                'user_details': serializer.data
            }
        else:
            response_data = {
                'message': f'The user {username} is not a teacher.',
                'user_details': serializer.data
            }

        return Response(response_data, status=status.HTTP_200_OK)
