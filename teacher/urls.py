# Author:littleZhao
# -*- codeing = utf-8 -*-
# @Time : 2021/5/14 17:21
# @Author : littleZhao
# @Site : 
# @File : urls.py
# @Software : PyCharm
from django.contrib import admin
from django.urls import path
from .views import BaseView, ReadMessage, MessageList, SheetsList, CreateSheetView, ReadSheet, LoginIndexView, \
    CreateTeacherView, StudentList, ReadStudent,StudentChartView

app_name = 'teacher'

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('login/', LoginIndexView.as_view(), name='login'),
    path('register/', CreateTeacherView.as_view(), name='register'),

    path('echart/<studentname>/', StudentChartView.as_view(), name='chart'),

    path('grade/All-Student/', StudentList.as_view(), name='students_list'),
    path('grade/<student_slug>/', ReadStudent.as_view(), name='one_student'),

    path('sheet/New/', CreateSheetView.as_view(), name='sheets'),
    path('sheet/All-Sheets/', SheetsList.as_view(), name='sheets_list'),
    path('sheet/<sheet_slug>/', ReadSheet.as_view(), name='one_sheet'),

    path('message/All-Messages/', MessageList.as_view(), name='messages_list'),
    path('message/<message_slug>/', ReadMessage.as_view(), name='one_message'),

]
"""
    All-Messages/ 与 <message_slug> 的顺序不能颠倒，ALl-Message在前，<message_slug>在后，这个先码一下
    """
