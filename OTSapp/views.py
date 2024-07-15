from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from OTSapp.models import *
import datetime


def welcomePage(request):
    

    return render(request, "index.html" )

@login_required(login_url='/login/')
def homePage(request, user_id):
    test = Test.objects.all()

    candidates = get_object_or_404(User, id=user_id)
    return render(request, "home.html", {'candidates' : candidates, 'tests':test})

@login_required(login_url='/login/')
def questionPaper(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = TestQuestions.objects.filter(TestName=test)
    return render(request, 'questions.html', {'questions': questions, 'test': test})


@login_required(login_url='/login/')
def result(request, test_id):
    test = Test.objects.get(id=test_id)
    testname = Test.objects.get(TestName = test.TestName)
    questions = TestQuestions.objects.filter(TestName=test)
    user = request.user
    candidate = Candidates.objects.get(username=user.username)
    result = Result(username=candidate,TestName = testname, date=datetime.date.today())
    right_answers = 0
    wrong_answers = 0
    for question in questions:
        answer = request.POST.get(f'question_{question.id}')
        if answer == question.rightAns:
            right_answers += 1
        else:
            wrong_answers += 1
    result.right = right_answers
    result.wrong = wrong_answers
    result.point = right_answers * 5
    result.save()
    return render(request, 'result.html', {'result': result})


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/') 

        user = authenticate(username = username , password = password)   

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        
        else:
            login(request , user)

            return redirect('/home/' + str(user.id) + '/')


    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('/login/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )

        user.set_password(password)
        user.save()

        Candidates.objects.create(
            username = user.username,
            name = user.first_name + " " + user.last_name,
            password = user.password
        )

        messages.info(request, 'Account created successfully')

        return redirect('/register/')
    

    return render(request, 'register.html')
