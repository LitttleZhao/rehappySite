# Author:littleZhao
# -*- codeing = utf-8 -*-
# @Time : 2021/5/14 17:21
# @Author : littleZhao
# @Site : 
# @File : urls.py
# @Software : PyCharm
from django.urls import path, include
from .views import BaseTestView, SheetBoardView, CreateMessageView, MessageList, ReadMessage, ReadSheet,CreateAnswerView,LoginIndexView

app_name = 'student'

urlpatterns = [
    path('', BaseTestView.as_view(), name='base'),
    path('login/',LoginIndexView.as_view(),name='login'),
    path('sheet/sheetboard/<studentname>/', SheetBoardView.as_view(), name='sheetboard'),
    path('message/New/<studentname>/', CreateMessageView.as_view(), name='messages'),
    path('message/All-Messages/<studentname>', MessageList.as_view(), name='messages_list'),
    path('sheet/one_sheet/<studentname>/<sheet_slug>/', CreateAnswerView.as_view(), name='one_sheet'),
    path('answer/New/<studentname>/', CreateAnswerView.as_view(), name='answers'),

    # path('sheet/<sheet_slug>/', CreateAnswerView.as_view(), name='one_sheet'),

    path('message/<studentname>/<message_slug>/', ReadMessage.as_view(), name='one_message'),
]
