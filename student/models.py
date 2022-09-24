import datetime

from django.db import models

# Create your models here.
from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
import time


class Student(models.Model):
    """
    这是学生的信息model
    """
    std_name = models.CharField(max_length=10)
    std_gender = models.CharField(max_length=10)
    std_age = models.IntegerField()
    std_id = models.CharField(max_length=10)
    std_class = models.CharField(max_length=20)
    std_college = models.CharField(max_length=20)


class Message(models.Model):
    """
    这是学生发送留言的Model类型
    """
    user = models.CharField(max_length=20, blank=True)

    title = models.CharField(max_length=20, blank=False)
    body = RichTextField(config_name='ckeditor')
    message_slug = models.SlugField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Provides a readable string representation of ClassNote object.
        """
        return f'{self.title}'

    def join_title(self):
        """
        Uses a ClassNote object's title to produce a lowercased version devoid
        of whitespaces and returns it as a string.
        """
        joined_title = ''.join(self.title.lower().split(' '))
        return joined_title


class Week(models.Model):
    whichweek = models.CharField(max_length=20, blank=False)
    week_slug = models.SlugField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Provides a readable string representation of Course object.
        """
        return f'{self.whichweek}'


class Answer(models.Model):
    """
    这是每个sheet答案的model类
    """
    title = models.CharField(max_length=20, blank=False)
    studentname = models.CharField(max_length=20, blank=False)
    answer = RichTextField(config_name='ckeditor')
    week = models.ForeignKey(Week, on_delete=models.CASCADE, null=True, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Provides a readable string representation of ClassNote object.
        """
        return f'{self.title}'

    def join_title(self):
        """
        Uses a ClassNote object's title to produce a lowercased version devoid
        of whitespaces and returns it as a string.
        """
        joined_title = ''.join(self.title.lower().split(' '))
        return joined_title


class Score(models.Model):
    """
    这是每个answer打分的model类
    """
    studentname = models.CharField(max_length=20, blank=False)
    week = models.CharField(max_length=10,blank=False)
    answerscore = models.FloatField()
