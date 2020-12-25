from django import forms
from .models import Document, Question_Data, Student_Data


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )



class NewStudentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )



class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
