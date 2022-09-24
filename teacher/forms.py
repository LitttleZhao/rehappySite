# Author:littleZhao
# -*- codeing = utf-8 -*-
# @Time : 2021/5/18 0:09
# @Author : littleZhao
# @Site : 
# @File : forms.py
# @Software : PyCharm
from django import forms
from .models import Sheet, Teacher


class TeacherLoginForm(forms.ModelForm):
    """
    forms for creating a new Teacher Object
    """
    fields = ('account', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tch_id'].label = 'account'
        self.fields['tch_password'].label = 'password'

    class Meta():
        """
        Fields of ClassNote model to appear on form
        """
        model = Teacher
        fields = ("tch_id", "tch_password")


class TeacherRegisterForm(forms.ModelForm):
    """
    forms for creating a new Teacher Object
    """
    fields = ('userid', 'username', 'password', 'college')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tch_id'].label = 'userid'
        self.fields['tch_name'].label = 'username'
        self.fields['tch_password'].label = 'password'
        self.fields['tch_college'].label = 'college'

    class Meta():
        """
        Fields of ClassNote model to appear on form
        """
        model = Teacher
        fields = ("tch_id", "tch_name", "tch_password", "tch_college")


class SheetForm(forms.ModelForm):
    """
    forms for creating a new Sheet Object
    """
    fields = ('title', 'body', 'week')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = ''
            self.fields['week'].widget.attrs.update({"week": "w-10"})
        self.fields['title'].widget.attrs.update({
            "placeholder": "Please enter a title"
        })
        self.fields['week'].empty_label = 'Select a week'

    class Meta():
        """
        Fields of Sheet model to appear on form
        """
        model = Sheet
        fields = ("title", "body", "week")
