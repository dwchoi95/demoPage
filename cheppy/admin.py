from atexit import register
from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Account)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'password', 'name', 'birth']
    search_fields = ['email', 'name', 'birth']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['assignment_no', 'title', 'deadline']
    search_fields = list_display


@admin.register(Testsuite)
class TestsuiteAdmin(admin.ModelAdmin):
    list_display = ['testcase_no', 'assignment_no', 'tc_no', 'open_tc']
    search_fields = list_display


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['submit_no', 'assignment_no', 'email', 'created_at']
    search_fields = list_display


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['grade_no', 'submit_no', 'state', 'score', 'result']
    search_fields = list_display

