from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('',views.index,name="index"),
    path('home',views.index,name="home"),
    path('home/',views.index,name="home"),
    #path('scripts',HomeView.as_view(),name="home"),
    #path('scripts/',HomeView.as_view(),name="home2"),
    path('tests',views.tests,name="tests"),
    path('tests/',views.tests,name="tests"),
    path('tests/<int:test_data_id>',views.detail,name="detail"),
    path('tests/<int:test_data_id>/',views.detail,name="detail"),
    path('test_results/<int:test_data_id>',views.test_results,name="test_results"),
    path('test_results/<int:test_data_id>/',views.test_results,name="test_results"),
    path('classes',views.classes,name="classes"),
    path('classes/',views.classes,name="classes"),
    path('classes/<int:class_data_id>',views.class_detail,name="class_detail"),
    path('classes/<int:class_data_id>/',views.class_detail,name="class_detail"),
    path('class/<str:teacher_username>',views.class_detail_from_teacher_username,name="class_detail_from_teacher_username"),
    path('class/<str:teacher_username>/',views.class_detail_from_teacher_username,name="class_detail_from_teacher_username"),

    path('students',views.students,name="students"),
    path('students/',views.students,name="students"),
    path('student/<int:student_data_id>',views.student_dashboard,name="student_dashboard"),
    path('student/<int:student_data_id>/',views.student_dashboard,name="student_dashboard"),
    path('u/<str:student_data_username>',views.student_dashboard_from_username,name="student_dashboard_from_username"),
    path('u/<str:student_data_username>/',views.student_dashboard_from_username,name="student_dashboard_from_username"),
    path('ready_tests/<str:student_data_username>',views.ready_tests,name="ready_tests"),
    path('ready_tests/<str:student_data_username>/',views.ready_tests,name="ready_tests"),

    path('run_test/<int:test_data_id>',views.process_run_test,name="run_test"),
    path('run_test/<int:test_data_id>/',views.process_run_test,name="run_test"),

    path('questions',views.questions,name="questions"),
    path('questions/',views.questions,name="questions"),
    path('question/<int:question_data_id>',views.question_detail,name="question_detail"),
    path('question/<int:question_data_id>/',views.question_detail,name="question_detail"),
    path('categories',views.categories,name="categories"),
    path('categories/',views.categories,name="categories"),
    path('category/<int:category_id>',views.category_detail,name="category_detail"),
    path('category/<int:category_id>/',views.category_detail,name="category_detail"),

    path('create_test',views.process_create_test,name="create_test"),
    path('create_test/',views.process_create_test,name="create_test"),
    path('create_question',views.process_create_question,name="create_question"),
    path('create_question/',views.process_create_question,name="create_question"),
    path('import_questions',views.import_questions,name="import_questions"),
    path('import_questions/',views.import_questions,name="import_questions"),
    path('import_test',views.import_test,name="import_test"),
    path('import_test/',views.import_test,name="import_test"),

    path('upload_questions',views.upload_questions,name="upload_questions"),
    path('upload_questions/',views.upload_questions,name="upload_questions"),
    path('upload_test',views.upload_test,name="upload_test"),
    path('upload_test/',views.upload_test,name="upload_test"),
    path('student_test_data/<int:student_data_id>', views.student_test_data, name='student_test_data-chart'),
    path('student_test_data/<int:student_data_id>/', views.student_test_data, name='student_test_data-chart'),

    path('download/<str:filename>', views.download_file,name="download_file")





]
