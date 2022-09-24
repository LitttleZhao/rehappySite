from django.db import models

# Create your models here.
from django.db import models
from ckeditor.fields import RichTextField
from django.db import models
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from student.models import Week

app_name = 'teacher'


class Teacher(models.Model):
    """
    这是老师的Model类型
    """
    tch_id = models.CharField(max_length=20, blank=False)
    tch_name = models.CharField(max_length=20, blank=False)
    tch_password = models.CharField(max_length=20, blank=False)
    tch_college = models.CharField(max_length=20, blank=False)


class Sheet(models.Model):
    """
    这是老师发送问题的Model类型
    """
    # user = models.CharField(max_length=20, blank=True)

    title = models.CharField(max_length=20, blank=False)
    '''这里的title可以表示这次的sheet主题是怎么样的，也可以表示这个sheet是什么时候发布的，比如：第一周、第二周之类的'''
    body = RichTextField(config_name='ckeditor')
    sheet_slug = models.SlugField(null=True)
    week = models.ForeignKey(Week, on_delete=models.CASCADE, null=True, related_name='sheets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Provides a readable string representation of Sheet object.
        """
        return f'{self.title}'

    def join_title(self):
        """
        Uses a Sheet object's title to produce a lowercased version devoid
        of whitespaces and returns it as a string.
        """
        joined_title = ''.join(self.title.lower().split(' '))
        return joined_title
