from django.contrib import admin
from .models import  Document, Test_Data, Question_Data, Question_Attempt, Student_Data, Class_Section, Class_Assignment, Category
# Register your models here.



# Register your models here.

admin.site.register(Test_Data)
admin.site.register(Student_Data)
admin.site.register(Question_Data)
admin.site.register(Question_Attempt)
admin.site.register(Class_Section)
admin.site.register(Class_Assignment)
admin.site.register(Category)
admin.site.register(Document)
