from dataclasses import field
from django import forms
from .models import *



class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'password', 'name', 'birth',)


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('assignment_no', 'title', 'problem', 'constraint', 'format',)


class TestsuiteForm(forms.ModelForm):
    class Meta:
        model = Testsuite
        fields = ('testcase_no', 'assignment_no', 'tc_no', 'in_tc', 'out_tc', 'open_tc',)


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('submit_no', 'assignment_no', 'email', 'program',)


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('grade_no', 'submit_no', 'state', 'score', 'passfail', 'hints', 'feedback', 'patch', 'result',)