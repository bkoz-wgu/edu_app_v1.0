import random
from . import models
from .models import Question_Data, Test_Data, Student_Data, Question_Attempt, Class_Section, Class_Assignment, Category
import math
from datetime import datetime
from django.http import JsonResponse
import json
import operator
from django.db.models import Q
import csv




class category_data:
    def __init__(self, id, student_score, id_list, included_bool):
        self.id = id
        self.student_score = student_score
        self.id_list = id_list
        self.included_bool = included_bool



def getStudentInClass(class_data_id):
    class_section = Class_Section.objects.filter(id=class_data_id)[0]
    class_assignments = Class_Assignment.objects.filter(class_section=class_section)
    student_filter = Q()
    for ca in class_assignments:
        student_filter = student_filter | Q(id=ca.student.id)
    return Student_Data.objects.filter(student_filter)


def getClassData(teacher_username):
    x = 0






def getQuestionData(question_id):
    question_detail = Question_Data.objects.filter(id=question_id)[0]
    total_attempts = Question_Attempt.objects.filter(question=question_detail).count()
    correct_attempts = Question_Attempt.objects.filter(question=question_detail, result="C").count()
    incorrect_attempts = Question_Attempt.objects.filter(question=question_detail, result="I").count()
    omitted_attempts = 0
    for attempt in Question_Attempt.objects.filter(question=question_detail, result="O"):
        if attempt.test.graded == True:
            omitted_attempts +=1
    answered_A = Question_Attempt.objects.filter(question=question_detail, user_answer="A").count()
    answered_B = Question_Attempt.objects.filter(question=question_detail, user_answer="B").count()
    answered_C = Question_Attempt.objects.filter(question=question_detail, user_answer="C").count()
    answered_D = Question_Attempt.objects.filter(question=question_detail, user_answer="D").count()
    data = {
        "total_attempts":total_attempts,
        "correct_attempts":correct_attempts,
        "incorrect_attempts":incorrect_attempts,
        "omitted_attempts":omitted_attempts,
        "answered_A":answered_A,
        "answered_B":answered_B,
        "answered_C":answered_C,
        "answered_D":answered_D
    }




def getStudentTestData(student_data_id):
        student_detail = Student_Data.objects.filter(id=student_data_id)[0]
        labels = []
        data = []
        test_ids = []
        test_scores = []
        cat1_scores = []
        cat2_scores = []
        cat3_scores = []
        cat4_scores = []
        goal_scores = []
        categories = Category.objects.order_by("pk")
        student_tests = Test_Data.objects.filter(student_username=student_detail.username).order_by("pk")
        labels = []
        labels.append("Overall Score")
        for cat in categories:
            labels.append(cat.category_name)

        for test in student_tests:
            test_ids.append(test.id)
            test_scores.append(test.score)
            cat1_scores.append(test.avg1)
            cat2_scores.append(test.avg2)
            cat3_scores.append(test.avg3)
            cat4_scores.append(test.avg4)
            goal_scores.append(test.goal_score)

        data={ 'labels': labels,
            'test_ids': test_ids,
            'test_scores': test_scores,
            'goal_scores': goal_scores,
            'cat1_scores': cat1_scores,
            'cat2_scores': cat2_scores,
            'cat3_scores': cat3_scores,
            'cat4_scores': cat4_scores,
        }

        return data




def createTest(jsonData):
    print(" Checkpoint 0")
    # get username from json
    import_student_username = jsonData["uname"]
    test_type = jsonData["test_type"]

    # create a new test_data object
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    this_student = Student_Data.objects.filter(username=import_student_username)[0]
    test_name_string = this_student.student_name + " - Test - " + now
    new_test = Test_Data.objects.create(
        test_name =  test_name_string,
        student_username =  this_student.username
        )
    new_test.save()
    import_test_id = Test_Data.objects.order_by("-pk")[0].id

    #Combine category and student data in dictionary
    cat_data = createCategoryData(import_student_username,jsonData);

    print(" Checkpoint 1")
    #Determine test_type and create question_List
    question_list = []
    if test_type == "CustomTest":
        question_list = createCustomTest(cat_data)
    elif test_type == "AlgoTest":
        if (Test_Data.objects.filter(student_username=import_student_username,graded=True).count() < 3):
            question_list = createAlgoTest(import_student_username, cat_data, [5,5,5,5])
        else:
            question_list =  createAlgoTest(import_student_username, cat_data,[7,6,5,4])

    # create question_attempt objects for each question in list
    print(" Checkpoint 2")

    for question in question_list:
            question_id = int(question)
            new_question_attempt = Question_Attempt.objects.create(
                question=Question_Data.objects.filter(id=question_id)[0],
                test=Test_Data.objects.filter(id=import_test_id)[0],
                user=Student_Data.objects.filter(username=import_student_username)[0],
                user_answer = "",
                result = "O"
                )
            new_question_attempt.save()



def createCategoryData(student_username, jsonData):
    #create id lists
    cat_1_ids = []
    cat_2_ids = []
    cat_3_ids = []
    cat_4_ids = []

    for question in Question_Data.objects.filter(category_id=1):
        cat_1_ids.append(question.id)
    for question in Question_Data.objects.filter(category_id=2):
        cat_2_ids.append(question.id)
    for question in Question_Data.objects.filter(category_id=3):
        cat_3_ids.append(question.id)
    for question in Question_Data.objects.filter(category_id=4):
        cat_4_ids.append(question.id)


    #randomize lists
    random.shuffle(cat_1_ids)
    random.shuffle(cat_2_ids)
    random.shuffle(cat_3_ids)
    random.shuffle(cat_4_ids)


    student_data =Student_Data.objects.filter(username=student_username)[0]
    cat1_score = student_data.average_t1
    cat2_score = student_data.average_t2
    cat3_score = student_data.average_t3
    cat4_score = student_data.average_t4


    cat1_bool = jsonData["cat1"]
    cat2_bool = jsonData["cat2"]
    cat3_bool = jsonData["cat3"]
    cat4_bool = jsonData["cat4"]


    #create category_data instances
    cat_1 = category_data(1, cat1_score, cat_1_ids, cat1_bool)
    cat_2 = category_data(2, cat2_score, cat_2_ids, cat2_bool)
    cat_3 = category_data(3, cat3_score, cat_3_ids, cat3_bool)
    cat_4 = category_data(4, cat4_score, cat_4_ids, cat4_bool)

    #create dictionary of instances
    cat_data = {}
    cat_data[cat_1.id] = cat_1
    cat_data[cat_2.id] = cat_2
    cat_data[cat_3.id] = cat_3
    cat_data[cat_4.id] = cat_4

    return cat_data




def createCustomTest(cat_data):
    #see which categories are chosen
    question_list = []
    c = 0
    per_test = {0:5, 1:20, 2:10, 3:6, 4:5}
    for cat in cat_data:
        if cat_data[cat].included_bool == "true":
            c += 1
    for cat in cat_data:
        if (cat_data[cat].included_bool == "true") or (c == 0):
            i = 0
            for question in cat_data[cat].id_list:
                if i < per_test[c]:
                    question_list.append(cat_data[cat].id_list[i])
                    i+=1
    return question_list





def createAlgoTest(student_username, cat_data, algo_ratio):
    question_list = []
    for cat in (sorted(cat_data, key=lambda item: cat_data[item].student_score, reverse=True)):
            col=0
            i = 0
            for question in cat_data[cat].id_list:
                if i < algo_ratio[col]:
                    question_list.append(cat_data[cat].id_list[i])
                    i+=1
                else:
                    break
            col+=1
    return question_list




def getAllTestQuestions(test_id):
    #see which categories are chosen
    print("fix")

    return question_list




def submitRunTest(data):
    # create object from json
    name_string ='tests/uploads/'+ data["uname"] + "_test_" + str(data["test_id"]) + ".csv"
    with open(name_string, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["student_username", data["uname"]])
        writer.writerow(["test_id", data["test_id"]])
        writer.writerow(["goal_score", data["goal"]])
        counter = 0
        for item in data:
            if counter < len(data)-3:
                writer.writerow([item, data[item]])
                counter +=1
    importStudentTest(name_string)





def createNewQuestion(jsonData):
        category_id = Category.objects.filter(category_name=jsonData['category'])[0].id
        new_question = Question_Data.objects.create(
            question_copy=jsonData['question_body'],
            category_id=category_id,
            question_choice_1 = jsonData['answer_choice_1'],
            question_choice_2 = jsonData['answer_choice_2'],
            question_choice_3 = jsonData['answer_choice_3'],
            question_choice_4 = jsonData['answer_choice_4'],
            correct_answer = jsonData['correct_answer']
            )
        new_question.save()




def createNewStudent():
    categories = Category.objects.filter()
    #create user
    #create student








def updateCategoryCounts():
    categories = Category.objects.filter()
    for category in categories:
        cat_count = Question_Data.objects.filter(category_id=category.id).count()
        Category.objects.filter(id=category.id).update(cat_count = cat_count)




def updateStudentStats(username):
    # Get student data
    student_query = Student_Data.objects.filter(username=username)
    this_student = Student_Data.objects.filter(username=username)[0]

    # get student test_data
    recent_tests = Test_Data.objects.filter(student_username=username, graded=True).order_by("-pk")

    if recent_tests.count() < 3:
       # Not enough Data to Caclulate
       x=1

    else:
        total_cat_1 = 0
        correct_cat_1 = 0
        total_cat_2 = 0
        correct_cat_2 = 0
        total_cat_3 = 0
        correct_cat_3 = 0
        total_cat_4 = 0
        correct_cat_4 = 0
        overall_total=0
        avg_cat_1 = 0
        avg_cat_2 = 0
        avg_cat_3 = 0
        avg_cat_4 = 0
        overall_avg = 0


        #find 4 section averages and overall average from most 3 recent Tests
        a = [1,1,1]
        for i in a:
            total_cat_1 += int(recent_tests[i].avg1)
            total_cat_2 += int(recent_tests[i].avg2)
            total_cat_3 += int(recent_tests[i].avg3)
            total_cat_4 += int(recent_tests[i].avg4)
            overall_total += int(recent_tests[i].score)



        avg_cat_1 = math.floor(total_cat_1/3)
        avg_cat_2 = math.floor(total_cat_2/3)
        avg_cat_3 = math.floor(total_cat_3/3)
        avg_cat_4 = math.floor(total_cat_4/3)
        overall_avg = math.floor(overall_total/3)

        student_query.update(
            average_total = overall_avg,
            average_t1 = avg_cat_1,
            average_t2 = avg_cat_2,
            average_t3 = avg_cat_3,
            average_t4 = avg_cat_4
        )






def importQuestions(csv_file_loc):
    # import file data by lines
    with open(csv_file_loc, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='|')
        # create new questions
        rowcount=0
        for row in csv_reader:
            if rowcount==0:
                #skip
                rowcount+=1
            else:
                import_copy= row[0]
                import_category= row[1]
                import_choice_1= row[2]
                import_choice_2= row[3]
                import_choice_3= row[4]
                import_choice_4= row[5]
                import_correct_answer= row[6]

                new_question = Question_Data.objects.create(
                    question_copy=import_copy,
                    category_id=import_category,
                    question_choice_1 = import_choice_1,
                    question_choice_2 = import_choice_2,
                    question_choice_3 = import_choice_3,
                    question_choice_4 = import_choice_4,
                    correct_answer = import_correct_answer
                    )
                new_question.save()
                rowcount+=1






def importStudentTest(csv_file_loc):
    # import file data by lines
    with open(csv_file_loc, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        # create new questions
        row_num = 0
        num_correct=0
        total_questions=0
        questions = Question_Data.objects
        import_test_id = "1"
        import_student_username = "n/a"
        total_cat_1 = 0
        correct_cat_1 = 0
        total_cat_2 = 0
        correct_cat_2 = 0
        total_cat_3 = 0
        correct_cat_3 = 0
        total_cat_4 = 0
        correct_cat_4 = 0
        goal_score = "n/a"
        avg_cat_1 = "n/a"
        avg_cat_2 = "n/a"
        avg_cat_3 = "n/a"
        avg_cat_4 = "n/a"
        new_score="n/a"


        for row in csv_reader:
            if row_num == 0:
                import_student_username= row[1].strip()
                row_num +=1
            elif row_num == 1:
                import_test_id= row[1].strip()
                if import_test_id=="new":
                    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    this_student = Student_Data.objects.filter(username=import_student_username)[0]
                    test_name_string = this_student.student_name + " - Test - " + now
                    new_test = Test_Data.objects.create(
                        test_name =  test_name_string,
                        student_username =  this_student.username
                        )
                    new_test.save()
                    import_test_id = Test_Data.objects.order_by("-pk")[0].id
                row_num +=1
            elif row_num == 2:
                goal_score= int(row[1].strip())
                row_num +=1

            else:
                total_questions +=1
                import_question_id= int(row[0].strip())
                import_user_answer= row[1].strip()
                this_question=Question_Data.objects.filter(id=import_question_id)[0]
                this_category = int(this_question.category_id)
                if this_category == 1:
                    total_cat_1 += 1
                elif this_category == 2:
                    total_cat_2 +=1
                elif this_category == 3:
                    total_cat_3 +=1
                elif this_category == 4:
                    total_cat_4 +=1


                if import_user_answer == "null":
                    calculated_result = "O"
                else:
                    this_correct_answer = questions.filter(id=import_question_id)[0].correct_answer
                    if this_correct_answer==import_user_answer:
                        calculated_result = "C"
                        num_correct +=1
                        if this_category == 1:
                            correct_cat_1 += 1
                        elif this_category == 2:
                            correct_cat_2 +=1
                        elif this_category == 3:
                            correct_cat_3 +=1
                        elif this_category == 4:
                            correct_cat_4 +=1
                    else:
                        calculated_result = "I"
                new_question_attempt = Question_Attempt.objects.create(
                    question=this_question,
                    test=Test_Data.objects.filter(id=import_test_id)[0],
                    user=Student_Data.objects.filter(username=import_student_username)[0],
                    user_answer = import_user_answer,
                    result = calculated_result
                    )
                new_question_attempt.save()
                row_num +=1

        # Get all test statistics
        if total_questions != 0:
            new_score = math.floor(num_correct/total_questions*100)
        if total_cat_1 != 0:
            avg_cat_1 = math.floor(correct_cat_1/total_cat_1*100)
        if total_cat_2 != 0:
            avg_cat_2 = math.floor(correct_cat_2/total_cat_2*100)
        if total_cat_3 != 0:
            avg_cat_3 = math.floor(correct_cat_3/total_cat_3*100)
        if total_cat_4 != 0:
            avg_cat_4 = math.floor(correct_cat_4/total_cat_4*100)


        this_test=Test_Data.objects.filter(id=import_test_id)
        if this_test.count() > 0:
            import_test_name = this_test[0].test_name
            this_test.update(
                test_name = "#"+ str(import_test_id) + " - "+ import_test_name,
            )
        this_test.update(
            score = new_score,
            avg1 = avg_cat_1,
            avg2 = avg_cat_2,
            avg3 = avg_cat_3,
            avg4 = avg_cat_4,
            goal_score= goal_score,
            graded = True
        )
        updateStudentStats(import_student_username)
