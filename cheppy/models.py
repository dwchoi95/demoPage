from django.db import models

# Create your models here.

class Account(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    birth = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


class Assignment(models.Model):
    assignment_no = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    problem = models.TextField()
    constraint = models.TextField()
    format = models.TextField()
    deadline = models.DateField()


class Testsuite(models.Model):
    testcase_no = models.AutoField(primary_key=True)
    assignment_no = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    tc_no = models.IntegerField()
    in_tc = models.TextField()
    out_tc = models.TextField()
    open_tc = models.BooleanField()


class Submission(models.Model):
    submit_no = models.AutoField(primary_key=True)
    assignment_no = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    email = models.ForeignKey(Account, on_delete=models.CASCADE)
    program = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


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