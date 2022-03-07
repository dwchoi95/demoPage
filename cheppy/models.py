from django.db import models

# Create your models here.

class Account(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


class Assignment(models.Model):
    LEVEL_CHOICES = (
        ('1', '초급'),
        ('2', '중급'),
        ('3', '상급'),
    )
    assignment_no = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    problem = models.TextField()
    constraint = models.TextField()
    format = models.TextField()
    answer = models.TextField()
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, default='1')
    timeout = models.IntegerField(default=1)


class Testsuite(models.Model):
    testcase_no = models.AutoField(primary_key=True)
    assignment_no = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    tc_no = models.IntegerField()
    in_tc = models.TextField()
    out_tc = models.TextField()
    open_tc = models.BooleanField(default=True)


class Submission(models.Model):
    submit_no = models.AutoField(primary_key=True)
    assignment_no = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    email = models.ForeignKey(Account, on_delete=models.CASCADE)
    program = models.TextField()
    attempt = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Solution(models.Model):
    solution_no = models.AutoField(primary_key=True)
    assignment_no = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    program = models.TextField()
    standardization = models.TextField(null=True, blank=True)
    specification = models.TextField(null=True, blank=True)
    


class Grade(models.Model):
    grade_no = models.AutoField(primary_key=True)
    submit_no = models.ForeignKey(Submission, on_delete=models.CASCADE)
    state = models.CharField(max_length=10)
    score = models.IntegerField()
    passfail = models.TextField()
    hints = models.TextField()
    feedback = models.TextField()
    patch = models.TextField()
    result = models.CharField(max_length=10)
    # attempt = models.IntegerField()

