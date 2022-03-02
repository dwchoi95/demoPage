from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Subquery
from http.client import HTTPResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth

import os, sys
from subprocess import check_output, STDOUT, CalledProcessError
import json
import tempfile

import warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.abspath(
            os.path.dirname(os.path.abspath(
                    os.path.dirname(__file__))))))
# from GraFee.grafee import *
# from GraFee.execution import *

from .models import *
from .forms import *

# Create your views here.
def main(request):
    email = request.session.get('email')
    if email:
        return render(request, 'cheppy/main.html', {
            'email' : email,
        })
    return render(request, 'cheppy/main.html')


def sign(request):
    error = None
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        birth = request.POST.get('birth')
        if not email:
            error = '이메일을 입력해주세요.'
        elif not password:
            error = '비밀번호를 입력해주세요.'
        elif not name:
            error = '이름을 입력해주세요.'
        elif not birth:
            error = '생년월일을 입력해주세요.'
        elif email:
            try:
                Account.objects.get(email=email)
                error = '이미 존재하는 이메일입니다.'
            except: pass
        elif birth:
            if len(birth) != 6:
                error = '생년월일을 6자리로 입력해주세요.'
        
        if error is None:
            account = Account()
            account.email = email
            account.password = password
            account.name = name
            account.birth = birth
            account.created_at = datetime.now()
            account.save()
            return render(request, 'cheppy/login.html', {
                'account' : account,
            })
        
        messages.error(request, error, extra_tags='danger')
        return render(request, 'cheppy/sign.html', {
                'email' : email,
                'password':password,
                'name':name,
                'birth':birth,
            })

    return render(request, 'cheppy/sign.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            account = Account.objects.get(email=email, password=password)
            if account:
                request.session['email'] = account.email
                return redirect(course)
        except: pass

        error = "이메일 혹은 비밀번호를 다시 확인해주세요."
        messages.error(request, error, extra_tags='danger')
        return HttpResponseRedirect('/login/')

    return render(request, 'cheppy/login.html')


def logout(request):
    request.session.clear()
    return redirect(main)


def course(request):
    email = request.session.get('email')
    
    if email:
        assignments = Assignment.objects.all()
        submissions = Submission.objects.filter(email=email)
        grades = Grade.objects.all()

        solved = False
        data = {}
        for assign in assignments:
            submitted = False
            for submit in submissions:
                if assign.assignment_no == submit.assignment_no.assignment_no:
                    for grade in grades:
                        if submit.submit_no == grade.submit_no.submit_no:
                            submitted = True
                            solved = True
                            data[assign] = {submit:grade}
            
            if not submitted:
                data[assign] = None
        
        return render(request, 'cheppy/course.html', {
            'email':email,
            'data':data,
            'solved':solved,
        })
    
    return render(request, 'cheppy/course.html')


def coding(request):
    email = request.session.get('email')
    
    if request.method == "POST":
        btn = ""
        
        if 'assignment_no' in request.POST:
            assignment_no = request.POST.get('assignment_no')
            request.session['assignment_no'] = assignment_no
        else:
            assignment_no = request.session.get('assignment_no')

        assignment = Assignment.objects.get(assignment_no=assignment_no)
        testcases = Testsuite.objects.filter(assignment_no=assignment_no)
        
        if "solve" in request.POST:
            btn = "solve"
            return render(request, 'cheppy/coding.html', {
                "email":email,
                'assignment':assignment,
                'testcases':testcases,
                'btn':btn
            })

        elif "solution" in request.POST:
            btn = "solution"
            submit_no = request.POST.get('submit_no')
            grade_no = request.POST.get('grade_no')

            submission = Submission.objects.get(submit_no=submit_no)
            grade = Grade.objects.get(grade_no=grade_no)

            code = open(submission.program).read()
            
            feedback = eval(grade.feedback)
            
            feed_length = 0
            for feed in feedback.values():
                feed_length += len(feed)

            return render(request, 'cheppy/coding.html', {
                "email":email,
                "assignment":assignment,
                'testcases':testcases,
                "code":code,
                "state":grade.state,
                "score":grade.score,
                "passfail":eval(grade.passfail),
                "feedback":feedback,
                "feed_length":feed_length,
                "patch":grade.patch,
                "result":grade.result,
                "diff":diff_2_str(code, grade.patch),
                "btn":btn,
            })

        assignment_path = "../Data/Refactory/Assignments/question_"+assignment_no+"/"
        file_name = email.split('@')[0]+'.py'
        submission_path = assignment_path+'submission/'+file_name
        code = request.POST.get('code')
        
        if "feed" in request.POST:
            btn = "feed"
            
            state = request.POST.get('state')
            score = request.POST.get('score')
            passfail = eval(request.POST.get('passfail'))
            feedback = eval(request.POST.get('feedback'))
            patch = request.POST.get('patch')
            result = request.POST.get('result')
            lineno = request.POST.get('lineno')
            edit = request.POST.get('edit')
            fix = request.POST.get('fix')

            code_list = code.split('\n')

            if edit == "Insert":
                code_list.insert(int(lineno)-1, fix)
            elif edit == "Delete":
                del code_list[int(lineno)-1]
            elif edit == "Replace":
                code_list[int(lineno)-1] = fix
            
            code = "\n".join(code_list)

            for line, feed_list in list(feedback.items()):
                del feed_list[0]
                if feed_list:
                    feedback[line] = feed_list
                else:
                    del feedback[line]
                break
            
            feed_length = 0
            for feed in feedback.values():
                feed_length += len(feed)

            return render(request, 'cheppy/coding.html', {
                "email":email,
                "assignment":assignment,
                'testcases':testcases,
                "code":code,
                "state":state,
                "score":score,
                "passfail":passfail,
                "feedback":feedback,
                "feed_length":feed_length,
                "result":result,
                "patch":patch,
                "diff":diff_2_str(code, patch),
                "btn":btn,
            })

        elif "execute" in request.POST:
            btn = "execute"
            
            with open(submission_path, 'w') as w:
                w.write(code)
            
            result = ""
            cmd = 'python ' + submission_path
            try: result = check_output(cmd, stderr=STDOUT, shell=True, universal_newlines=True)
            except CalledProcessError as err: result = err.output.strip().split('\n')[-1]

            if not result:
                result = "아무런 출력값이 없습니다."
            
            return render(request, 'cheppy/coding.html', {
                "email":email,
                "assignment":assignment,
                'testcases':testcases,
                "code":code,
                "result":result,
                "btn":btn,
            })

        else:
            try: code = regular(code)
            except:
                return render(request, 'cheppy/coding.html', {
                    "email":email,
                    "assignment":assignment,
                    'testcases':testcases,
                    "code":code,
                    "result":"오류가 있어 실행할 수 없습니다.\n코드를 확인해주세요.",
                    "btn":"error",
                })

            func_map = get_func_map(code)
            
            code = ""
            for f_name, f_code in func_map.items():
                if f_name == "main":
                    continue
                code += '\n\n' + f_code
            if "main" in func_map.keys():
                code += '\n\n' + func_map["main"]

            code = regular(code)
            
            with open(submission_path, 'w') as w:
                w.write(code)

            gf = GraFee(assignment_path, [submission_path], 1)
            state_map, d_score_map, s_score_map, passfail_map, hints_map, patch_map, result_map, feedback_map = gf.run()
            
            state = state_map[file_name]
            d_score = d_score_map[file_name]
            passfail = passfail_map[file_name]
            hints = hints_map[file_name]
            feedback = feedback_map[file_name]
            patch = patch_map[file_name]
            result = result_map[file_name]

            diff = diff_2_str(code, patch)

            hint_length = 0
            for hint in hints.values():
                hint_length += len(hint)
            
            feed_length = 0
            for feed in feedback.values():
                feed_length += len(feed)

            if "grading" in request.POST:
                btn = "grading"
            elif "submit" in request.POST:
                btn = "submit"

                submission = Submission()
                submission.assignment_no = assignment
                submission.email = Account.objects.get(email=email)
                submission.program = submission_path
                submission.created_at = datetime.now()
                submission.save()

                grade = Grade()
                grade.submit_no = submission
                grade.state = state
                grade.score = d_score
                grade.passfail = passfail
                grade.hints = hints
                grade.feedback = feedback
                grade.patch = patch
                grade.result = result
                grade.save()
                
            return render(request, 'cheppy/coding.html', {
                "email":email,
                "assignment":assignment,
                'testcases':testcases,
                "code":code,
                "state":state,
                "score":d_score,
                "passfail":passfail,
                "hints":hints,
                "hint_length":hint_length,
                "feedback":feedback,
                "feed_length":feed_length,
                "patch":patch,
                "result":result,
                "diff":diff,
                "btn":btn,
            })

    return render(request, 'cheppy/coding.html')


def survey(request):
    return render(request, 'cheppy/survey.html')


def diff_2_str(submission, solution):
    diff2str = ""
    diff_list = list(difflib.unified_diff(
                submission.splitlines(keepends=True), solution.splitlines(keepends=True)))
        
    if diff_list:
        diff_list.insert(0, "diff --git submission solution")
        diff_list[1] = "--- submission"
        diff_list[2] = "+++ solution"
        diff_list = [diff.strip() for diff in diff_list if diff.strip()]
        diff2str = "\n".join(diff_list)
            
    return diff2str

def test_page(request):
    return render(request, 'cheppy/test_page.html')