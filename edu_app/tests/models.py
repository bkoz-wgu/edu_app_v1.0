from django.db import models



class Category(models.Model):
    category_name =  models.CharField(max_length=60)
    category_description =  models.CharField(max_length=400)
    cat_count =  models.CharField(max_length=10)
    def __str__(self):
        return self.category_name


class Question_Data(models.Model):
    question_copy = models.CharField(max_length=500)
    question_choice_1 = models.CharField(max_length=200)
    question_choice_2 = models.CharField(max_length=200)
    question_choice_3 = models.CharField(max_length=200)
    question_choice_4 = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1)
    category_id = models.CharField(max_length=1)


    def __str__(self):
        return self.question_copy

class Test_Data(models.Model):
    questions = models.ManyToManyField(Question_Data, through='Question_Attempt')
    score =  models.CharField(max_length=3, default="n/a")
    test_name =  models.CharField(max_length=60)
    graded = models.BooleanField(default=False)
    student_username =  models.CharField(max_length=20)
    avg1 =  models.CharField(max_length=3, default="n/a")
    avg2 =  models.CharField(max_length=3, default="n/a")
    avg3 =  models.CharField(max_length=3, default="n/a")
    avg4 =  models.CharField(max_length=3, default="n/a")
    goal_score = models.CharField(max_length=3, default="n/a")



    def __str__(self):
        return self.test_name

class Student_Data(models.Model):
    student_name =  models.CharField(max_length=60)
    username =  models.CharField(max_length=60)
    average_total = models.CharField(max_length=3)
    average_t1 = models.CharField(max_length=3)
    average_t2 = models.CharField(max_length=3)
    average_t3 = models.CharField(max_length=3)
    average_t4 = models.CharField(max_length=3)
    tests = models.ManyToManyField(Test_Data, through='Question_Attempt')

    def __str__(self):
        return self.student_name

class Question_Attempt(models.Model):
    test = models.ForeignKey(Test_Data, on_delete=models.CASCADE)
    question = models.ForeignKey(Question_Data, on_delete=models.CASCADE)
    user = models.ForeignKey(Student_Data, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=1)
    result = models.CharField(max_length=1, default="O")
    def __str__(self):
        return "Attempt: " + self.test.test_name + " - " + self.question.question_copy


class Class_Section(models.Model):
    students = models.ManyToManyField(Student_Data, through='Class_Assignment')
    section_name =  models.CharField(max_length=60)
    teacher_username = models.CharField(max_length=30)

    def __str__(self):
        return self.section_name


class Class_Assignment(models.Model):
    student = models.ForeignKey(Student_Data, on_delete=models.CASCADE)
    class_section = models.ForeignKey(Class_Section, on_delete=models.CASCADE)
    def __str__(self):
        return self.student.student_name + " - " + self.class_section.section_name


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
