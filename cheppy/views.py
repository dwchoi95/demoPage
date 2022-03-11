from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Subquery
from http.client import HTTPResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth


from collections import OrderedDict
from io import StringIO
import warnings
import os, sys
import difflib

warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from GraFee.core import *

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


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')

        try:
            account = Account.objects.get(email=email, name=name)
            if account:
                request.session['email'] = account.email
                request.session['name'] = account.name
                return redirect(course)
        except: pass

        try:
            account = Account()
            account.email = email
            account.name = name
            account.save()
            request.session['email'] = account.email
            request.session['name'] = account.name
            return redirect(course)
        except:
            error = "이미 존재하는 이메일입니다."
            messages.error(request, error, extra_tags='danger')
            return HttpResponseRedirect('/login/')

    return render(request, 'cheppy/login.html')


def logout(request):
    request.session.clear()
    return redirect(main)


def course(request):
    email = request.session.get('email')
    name = request.session.get('name')
    
    if request.method == "POST":
        assignment_no = request.POST.get('assignment_no')
        request.session['assignment_no'] = assignment_no
        
        if 'solution' in request.POST:
            return redirect(solution)

        return redirect(coding)

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
            'name':name,
            'data':data,
            'solved':solved,
        })
    
    return render(request, 'cheppy/course.html')


def coding(request):
    email = request.session.get('email')
    name = request.session.get('name')
    assignment_no = request.session.get('assignment_no')
    
    if assignment_no:
        assignment = Assignment.objects.get(assignment_no=assignment_no)
        testsuite = Testsuite.objects.filter(assignment_no=assignment_no)
        
        testsuite_map = {}
        for testcase in testsuite:
            if testcase.open_tc:
                testsuite_map[testcase.tc_no] = (testcase.in_tc, testcase.out_tc)
        
        testsuite_map = OrderedDict(sorted(testsuite_map.items()))

        if request.method == "POST":
            btn = "execute"
            code = request.POST.get('code')
            print(code)

            try: compile(code, "<string>", "exec")
            except:
                return render(request, 'cheppy/coding.html', {
                    "email":email,
                    'name':name,
                    "assignment":assignment,
                    'testsuite':testsuite_map,
                    "code":code,
                    "result":"오류가 있어 실행할 수 없습니다.\n코드를 확인해주세요.",
                    "btn":btn,
                })

            if "execute" in request.POST:
                btn = "execute"
                
                backup_stdout = sys.stdout
                sys.stdout = StringIO()

                try:
                    exec(code, globals())
                except Exception as e:
                    print(e)

                result = sys.stdout.getvalue().strip()

                if sys.stdout != backup_stdout:
                    sys.stdout.close()
                    sys.stdout = backup_stdout

                if not result or result == "None":
                    result = "출력되는 값이 없습니다.\n함수를 호출하고 있는지, 반환(return) 되는 값이 있는지 확인해보세요."
                
                return render(request, 'cheppy/coding.html', {
                    "email":email,
                    'name':name,
                    "assignment":assignment,
                    'testsuite':testsuite_map,
                    "code":code,
                    "result":result,
                    "btn":btn,
                })

            solutions = {}
            for sol in Solution.objects.filter(assignment_no=assignment_no):
                try:
                    sub = Submission.objects.get(program=sol.program)
                    solutions[sub.submit_no] = (sol.program, sol.standardization, sol.specification)
                except: pass
                
            programs = {}
            attempt = 0
            for submit in Submission.objects.filter(assignment_no=assignment_no, email=email):
                if submit.attempt > attempt:
                    attempt = submit.attempt

            submission = Submission()
            submission.assignment_no = assignment
            submission.email = Account.objects.get(email=email)
            submission.program = code
            submission.attempt = attempt + 1
            submission.created_at = datetime.now()
            submission.save()

            programs[submission.submit_no] = code
            
            testsuite = {}
            for testcase in Testsuite.objects.filter(assignment_no=assignment_no):
                testsuite[testcase.tc_no] = (testcase.in_tc, testcase.out_tc)

            gf = GraFee(solutions, assignment.format, {'reference':assignment.answer}, programs, testsuite, assignment.timeout)
            code_map, state_map, d_score_map, s_score_map, passfail_map, hints_map, patch_map, result_map, feedback_map, predata_map = gf.run()
            
            code = code_map[submission.submit_no]
            state = state_map[submission.submit_no]
            d_score = d_score_map[submission.submit_no]
            passfail = passfail_map[submission.submit_no]
            hints = hints_map[submission.submit_no]
            feedback = feedback_map[submission.submit_no]
            patch = patch_map[submission.submit_no]
            result = result_map[submission.submit_no]

            diff = diff_2_str(code, patch)

            hint_length = 0
            for hint in hints.values():
                hint_length += len(hint)
                
            submission = Submission.objects.get(submit_no=submission.submit_no)
            submission.program = code
            submission.save()
            
            if state == 'correct':
                predata = predata_map[submission.submit_no]
                for (p_code, p_st_code, p_spec) in predata.values():
                    solution_db = Solution()
                    solution_db.assignment_no = assignment
                    solution_db.program = p_code
                    solution_db.standardization = p_st_code
                    solution_db.specification = p_spec
                    
                    solution_db.save()

            if "grading" in request.POST:
                btn = "grading"
                
                return render(request, 'cheppy/coding.html', {
                    "email":email,
                    'name':name,
                    "assignment":assignment,
                    'testsuite':testsuite_map,
                    "code":code,
                    "state":state,
                    "score":d_score,
                    "passfail":passfail,
                    "hints":hints,
                    "hint_length":hint_length,
                    "patch":patch,
                    "result":result,
                    "diff":diff_2_str(code, patch),
                    "btn":btn,
                })
            elif "submit" in request.POST:
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

                return redirect(solution)

        return render(request, 'cheppy/coding.html', {
            "email":email,
            'name':name,
            "assignment":assignment,
            'testsuite':testsuite_map,
            "btn":"execute",
        })

    return render(request, 'cheppy/coding.html')


def solution(request):
    email = request.session.get('email')
    name = request.session.get('name')
    assignment_no = request.session.get('assignment_no')
    
    if assignment_no:
        assignment = Assignment.objects.get(assignment_no=assignment_no)
        testsuite = Testsuite.objects.filter(assignment_no=assignment_no)

        testsuite_map = {}
        for testcase in testsuite:
            if testcase.open_tc:
                testsuite_map[testcase.tc_no] = (testcase.in_tc, testcase.out_tc)
        
        testsuite_map = OrderedDict(sorted(testsuite_map.items()))

        if request.method == "POST":
            btn = "feed"

            code = request.POST.get('code')
            
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

            return render(request, 'cheppy/solution.html', {
                "email":email,
                'name':name,
                "assignment":assignment,
                'testsuite':testsuite_map,
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

        else:
            btn = "solution"

            assignments = Assignment.objects.all()
            submissions = Submission.objects.filter(email=email)
            grades = Grade.objects.all()

            submissions = Submission.objects.filter(email=email, assignment_no=assignment_no)

            submit_no = 0
            code = ''
            for submit in submissions:
                if assignment.assignment_no == submit.assignment_no.assignment_no:
                    submit_no = submit.submit_no
                    code = submit.program

            grade = Grade.objects.get(submit_no=submit_no)
            feedback = eval(grade.feedback)
            
            feed_length = 0
            for feed in feedback.values():
                feed_length += len(feed)

            return render(request, 'cheppy/solution.html', {
                "email":email,
                'name':name,
                "assignment":assignment,
                'testsuite':testsuite_map,
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

    return render(request, 'cheppy/solution.html')


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
