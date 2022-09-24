# Author:littleZhao
# -*- codeing = utf-8 -*-
# @Time : 2021/5/16 0:04
# @Author : littleZhao
# @Site : 
# @File : forms.py
# @Software : PyCharm
from django import forms
from .models import Message, Answer, Student


class StudentForm(forms.ModelForm):
    """
    forms for creating a new Message Object
    """
    fields = ('name', 'gender', 'age', 'id', 'class', 'college')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['std_name'].label = 'name'
        self.fields['std_gender'].label = 'gender'
        self.fields['std_age'].label = 'age'
        self.fields['std_id'].label = 'id'
        self.fields['std_class'].label = 'class'
        self.fields['std_college'].label = 'college'

    class Meta():
        """
        Fields of ClassNote model to appear on form
        """
        model = Student
        fields = ("std_name", "std_gender", "std_age", "std_id", "std_class", "std_college")


class MessageForm(forms.ModelForm):
    """
    forms for creating a new Message Object
    """
    fields = ('user','title', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = ''

        self.fields['title'].widget.attrs.update({
            "placeholder": "Please enter a title"
        })


    class Meta():
        """
        Fields of ClassNote model to appear on form
        """
        model = Message
        fields = ("title", "body")


class AnswerForm(forms.ModelForm):
    """
    forms for creating a new Sheet Object
    """
    fields = ('answer',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = ''

    class Meta():
        """
        Fields of Sheet model to appear on form
        """
        model = Answer
        fields = ("answer",)
