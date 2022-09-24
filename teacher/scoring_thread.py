# Author:littleZhao
# -*- codeing = utf-8 -*-
# @Time : 2021/5/23 15:08
# @Author : littleZhao
# @Site : 
# @File : scoring_thread.py
# @Software : PyCharm
import time
import threading
from student.models import Answer


class PrintThread(threading.Thread):

    def run(self):
        self.get
        queryset = Answer.objects.filter()
