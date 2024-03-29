from django.urls import path
from .views import UserRegistration, TeacherDetailView, IsTeacherAPIView, TeacherListAPIView, TeacherEditAPIView, \
    AddStudentToTeacher, StudentListView, CheckUsernameInStudentListView, AddReview, TeacherReviewStudentsAPIView, \
    TeacherSearch, UserDetailView

urlpatterns = [
    path('register/user', UserRegistration.as_view(), name='user_registration'),
    path('teacherdetail/<str:username>', TeacherDetailView.as_view(), name='teacher_detail'),
    path('is_teacher/<str:username>', IsTeacherAPIView.as_view(), name='is_teacher_api'),
    path('teacherslist', TeacherListAPIView.as_view(), name='teacher-list'),
    path('edit/teacher', TeacherEditAPIView.as_view(), name='teacher_edit'),
    path('add_student_to_teacher', AddStudentToTeacher.as_view(), name='add-student-to-teacher'),
    path('studentsdata/<str:teacher_username>', StudentListView.as_view(), name='student_list'),
    path('check_username', CheckUsernameInStudentListView.as_view(), name='check_username'),
    path('add_review', AddReview.as_view(), name='add_review'),
    path('teachers/<str:username>/reviewed_students', TeacherReviewStudentsAPIView.as_view(), name='teacher_reviewed_students'),
    path('searchteachers', TeacherSearch.as_view(), name='teacher_search'),
    path('user_details', UserDetailView.as_view(), name='user-detail'),
]
