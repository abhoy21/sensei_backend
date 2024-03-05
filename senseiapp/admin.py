from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Teacher, Student, Review


class UserAdmin(BaseUserAdmin):
    list_display = ('id','username', 'first_name', 'last_name', 'email', 'is_teacher')
    list_filter = ['is_teacher']
    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'imageURL', 'bio', 'whatsapp_number', 'latitude', 'longitude', 'is_teacher')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'imageURL', 'bio', 'whatsapp_number', 'latitude', 'longitude', 'is_teacher', 'is_student', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )

    filter_horizontal = ('groups', 'user_permissions',)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'qualifications')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'which_class')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id',  'rating', 'content')
    search_fields = ('id', 'content')


admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.unregister(Group)  # Unregister Group model
