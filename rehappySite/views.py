# Author:littleZhao
# -*- codeing = utf-8 -*-
# @Time : 2021/5/19 1:53
# @Author : littleZhao
# @Site : 
# @File : views.py
# @Software : PyCharm
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'
