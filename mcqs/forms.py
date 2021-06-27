from django import forms

from .models import Test

class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ('name','topic', 'number_of_questions','time','passing_score')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass form-control', 'title': 'Name'}),
            'topic': forms.TextInput(attrs={'class': 'textinputclass form-control', 'title': 'Topic'}),
            'number_of_questions': forms.NumberInput(attrs={'class': 'form-control', 'title': 'Number of Questions', 'min':'1'}),
            'time': forms.NumberInput(attrs={'class': 'form-control', 'title':'Time', 'placeholder':'Duration of test in minutes', 'min':'1'}),
            'passing_score':forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Required score in %', 'min':'1', 'max':'100'}),
        }

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder':'Upload a Word file in .docx format'}))
