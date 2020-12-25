from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .functions import *
from os.path import dirname as up
from django.views.decorators.csrf import csrf_exempt
import mimetypes
import os
from django.views.static import serve


from .models import Document, Question_Data, Test_Data, Student_Data, Question_Attempt, Class_Section, Class_Assignment, Category
from .forms import DocumentForm


# Create your views here.

def index(request):
    return render(request, 'tests/index.html')


def tests(request):
    tests = Test_Data.objects.order_by("-pk")
    return render(request, 'tests/tests.html', {'tests':tests})


def classes(request):
    classes = Class_Section.objects.order_by("-pk")
    return render(request, 'tests/classes.html', {'classes':classes})



def detail(request,test_data_id):
    test_detail = get_object_or_404(Test_Data,pk=test_data_id)
    question_attempts = Question_Attempt.objects.filter(test=test_data_id)
    my_filter_qs = Q()
    for qa in question_attempts:
        my_filter_qs = my_filter_qs | Q(question_copy=qa.question)
    questions = Question_Data.objects.filter(my_filter_qs)
    return render(request, 'tests/detail.html', {'test':test_detail, 'questions':questions})

def test_results(request,test_data_id):
    test_detail = get_object_or_404(Test_Data,pk=test_data_id)
    question_attempts = Question_Attempt.objects.filter(test=test_data_id)
    my_filter_qs = Q()
    for qa in question_attempts:
        my_filter_qs = my_filter_qs | Q(question_copy=qa.question)
    questions = Question_Data.objects.filter(my_filter_qs).order_by("pk")
    student = Student_Data.objects.filter(username=test_detail.student_username)[0]
    return render(request, 'tests/test_result.html', {'test':test_detail, 'questions':questions, 'question_attempts':question_attempts, 'student':student})


def class_detail(request,class_data_id):
    class_detail = get_object_or_404(Class_Section,pk=class_data_id)
    students = getStudentInClass(class_data_id)
    return render(request, 'tests/class_dashboard.html', {'class':class_detail, 'students':students})


def class_detail_from_teacher_username(request,teacher_username):
    class_detail =  Class_Section.objects.filter(teacher_username=teacher_username)
    if class_detail.count() < 1:
        return render(request, 'tests/index.html')
    else:
        class_data_id = Class_Section.objects.filter(teacher_username=teacher_username)[0].id
        students = getStudentInClass(class_data_id)
        return render(request, 'tests/class_dashboard.html', {'class':class_detail[0], 'students':students})





def students(request):
    students = Student_Data.objects.order_by("pk")
    return render(request, 'tests/students.html', {'students':students})

def student_dashboard(request,student_data_id):
    categories = Category.objects.order_by("pk")
    student_detail = get_object_or_404(Student_Data,pk=student_data_id)
    student_tests = Test_Data.objects.filter(student_username=student_detail.username, graded=True).order_by("-pk")
    ungraded_tests = Test_Data.objects.filter(student_username=student_detail.username, graded=False).order_by("pk")
    return render(request, 'tests/student_dashboard.html', {'student':student_detail, 'tests': student_tests,'ungraded_tests': ungraded_tests,'categories':categories})


def student_dashboard_from_username(request,student_data_username):
    student_data =Student_Data.objects.filter(username=student_data_username)[0]
    categories = Category.objects.order_by("pk")
    student_detail = get_object_or_404(Student_Data,pk=student_data.id)
    student_tests = Test_Data.objects.filter(student_username=student_detail.username, graded=True).order_by("-pk")
    ungraded_tests = Test_Data.objects.filter(student_username=student_detail.username, graded=False).order_by("pk")
    return render(request, 'tests/student_dashboard.html', {'student':student_detail, 'tests': student_tests, 'ungraded_tests': ungraded_tests,'categories':categories})



def ready_tests(request,student_data_username):
    student_data =Student_Data.objects.filter(username=student_data_username)[0]
    categories = Category.objects.order_by("pk")
    student_detail = get_object_or_404(Student_Data,pk=student_data.id)
    student_tests = Test_Data.objects.filter(student_username=student_detail.username, graded=False).order_by("pk")
    student_has_no_tests = False
    if student_tests.count() <1:
        student_has_no_tests = True
    return render(request, 'tests/ready_tests.html', {'student':student_detail, 'tests': student_tests,'categories':categories, 'student_has_no_tests': student_has_no_tests})



def student_test_data(request,student_data_id):
    student_detail = get_object_or_404(Student_Data,pk=student_data_id)
    dict_data = getStudentTestData(student_data_id)
    return JsonResponse(dict_data)




def questions(request):
    questions = Question_Data.objects.order_by("-pk")
    return render(request, 'tests/questions.html', {'questions':questions})

def question_detail(request,question_data_id):
    question_detail = get_object_or_404(Question_Data,pk=question_data_id)
    category = Category.objects.filter(id=question_detail.category_id)[0].category_name
    q_data = getQuestionData(question_data_id)
    return render(request, 'tests/question-detail.html', {'question':question_detail, "q_data":q_data, "category":category})




def categories(request):
    categories = Category.objects.order_by("pk")
    updateCategoryCounts();
    return render(request, 'tests/categories.html', {'categories':categories})

def category_detail(request,category_id):
    category_detail = get_object_or_404(Category,pk=category_id)
    cat_questions = Question_Data.objects.filter(category_id=category_id).order_by("pk")
    return render(request, 'tests/category-detail.html', {'category':category_detail, 'questions':cat_questions})


def run_test(request,test_data_id):
    test_detail = get_object_or_404(Test_Data,pk=test_data_id)
    question_attempts = Question_Attempt.objects.filter(test=test_data_id)
    my_filter_qs = Q()
    for qa in question_attempts:
        my_filter_qs = my_filter_qs | Q(question_copy=qa.question)
    questions = Question_Data.objects.filter(my_filter_qs).order_by("pk")

    return render(request, 'tests/run_test.html', {'test':test_detail, 'question_attempts':   question_attempts, 'questions':   questions})


def import_questions(request):
    categories = Category.objects.order_by("pk")
    test_name= 'tests/uploads/test_name.csv'
    importQuestions(test_name)
    return render(request, 'tests/index.html', {'categories':categories})



def import_test(request):
    categories = Category.objects.order_by("pk")
    test_name= 'tests/uploads/test_name.csv'
    importStudentTest(test_name)
    tests = Test_Data.objects.order_by("pk")
    return render(request, 'tests/tests.html', {'tests':tests})




def write_test_to_csv(request):
    gradeTest();
    tests = Test_Data.objects.order_by("pk")
    return render(request, 'tests/tests.html', {'tests':tests})





def scripts(request):
    return render(request, 'tests/scripts.html')


def login(request):
    test = Test_Data.objects.order_by("pk")[0]
    return render(request, 'tests/login.html', {'test':test})




def user_dashboard(request,user_id):
    tests = Test_Data.objects.order_by("pk")
    user_detail = get_object_or_404(User,pk=user_id)
    return render(request, 'tests/student_dashboard.html', {'user':user_detail, 'tests':tests})

def tutor_dashboard(request,user_id):
    user_detail = get_object_or_404(User,pk=user_id)
    return render(request, 'tests/tutor_dashboard.html', {'user':user_detail})







@csrf_exempt
def process_run_test(request,test_data_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        del data['csrfmiddlewaretoken']
        submitRunTest(data)
        return render(request, "tests/run_test.html", {"message":"Upload Successful"})
    else:
        test_detail = get_object_or_404(Test_Data,pk=test_data_id)
        question_attempts = Question_Attempt.objects.filter(test=test_data_id)
        my_filter_qs = Q()
        for qa in question_attempts:
            my_filter_qs = my_filter_qs | Q(question_copy=qa.question)
        questions = Question_Data.objects.filter(my_filter_qs).order_by("pk")
    return render(request, 'tests/run_test.html', {'test':test_detail, 'question_attempts':   question_attempts, 'questions':   questions})




@csrf_exempt
def process_create_test(request):
    categories = Category.objects.order_by("pk")

    if request.method == 'POST':
        data = json.loads(request.body)
        del data['csrfmiddlewaretoken']
        entered_username = data["uname"]
        respond_data = { 'user_valid': Student_Data.objects.filter(username__iexact=entered_username).exists() }
        if respond_data['user_valid']:
            createTest(data)
            return JsonResponse(respond_data)
        else:
            data['error_message'] = 'A user with this username already exists.'
            return JsonResponse(respond_data)
    return render(request, 'tests/create_test.html', {'categories':categories})






@csrf_exempt
def process_create_question(request):
    categories = Category.objects.order_by("pk")

    if request.method == 'POST':
        data = json.loads(request.body)
        del data['csrfmiddlewaretoken']
        cateogry_valid = (data["category"] != "null")
        correct_answer_valid = (data["correct_answer"]  != "null")
        empty_blanks_found = (data['answer_choice_1']=="") or (data['answer_choice_2']=="") or  (data['answer_choice_3']=="") or  (data['answer_choice_4']=="") or  (data['question_body']=="")
        question_is_default = (data['question_body']=="Enter the body of your question here.")
        is_all_data_valid = cateogry_valid and correct_answer_valid and ~(empty_blanks_found) and ~(question_is_default)


        respond_data = {
            'is_valid_correct_answer' : correct_answer_valid,
            'is_valid_category' :cateogry_valid,
            'empty_blanks_found': empty_blanks_found,
            'question_is_default': question_is_default,
            'is_all_data_valid' : is_all_data_valid
            }

        if respond_data['is_all_data_valid']:
            #print(data)
            createNewQuestion(data)
            return JsonResponse(respond_data)
        else:
            data['error_message'] = 'There is an error in your submission.'
            return JsonResponse(respond_data)
    return render(request, 'tests/create_question.html', {'categories':categories})





def upload_test(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            test_name= 'tests/' + Document.objects.order_by("-pk")[0].document.name
            importStudentTest(test_name)
            return render(request, "tests/upload_test.html", {"message":"Upload Successful"})
    else:
        form = DocumentForm()
    return render(request, 'tests/upload_test.html', {
        'form': form
    })


def upload_questions(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            doc_name= 'tests/' + Document.objects.order_by("-pk")[0].document.name
            importQuestions(doc_name)
            return render(request, "tests/upload_questions.html", {"message":"Upload Successful"})
    else:
        form = DocumentForm()
    return render(request, 'tests/upload_questions.html', {
        'form': form
    })





def download_file(request, filename):
    # fill these variables with real values
    filepath = 'tests/public_downloads/' + filename
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
