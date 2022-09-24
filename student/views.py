from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, resolve_url, get_object_or_404
from django.template.defaultfilters import striptags
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from .models import Message
from teacher.models import Sheet
from .models import Student
from .forms import MessageForm, AnswerForm, StudentForm


class BaseTestView(ListView):
    template_name = 'student/base_std.html'

    def get_queryset(self):
        return None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BaseTestView, self).get_context_data()
        context['student'] = True
        return context


class LoginIndexView(FormView):
    """
    Simple view for student login.
    """
    template_name = 'student/login.html'
    form_class = StudentForm
    success_url = reverse_lazy("student:sheetboard")

    def form_valid(self, form):
        student_form = StudentForm(self.request.POST)
        student = student_form.save(commit=False)
        student.save()
        student_slug = get_object_or_404(Student, std_id=student.std_id)
        print(student_slug.std_name + "  我也不知道有没有")
        return HttpResponseRedirect(reverse("student:sheetboard", kwargs={"studentname": student.std_name}))


class CreateAnswerView(CreateView, DetailView):
    """
    View for creating new message object.
    """
    template_name = 'student/answers.html'
    context_object_name = 'sheet'
    form_class = AnswerForm
    success_url = reverse_lazy("student:sheetboard")

    def form_valid(self, form):
        """
        Instantiates a new Message object given a valid form.
        """
        student = get_object_or_404(Student, std_name=self.kwargs['studentname'])
        answer_form = AnswerForm(self.request.POST)
        answer = answer_form.save(commit=False)
        answer.title = self.request.POST['title']
        answer.week_id=self.request.POST['week_slug']
        answer.studentname = student.std_name
        answer.save()
        return HttpResponseRedirect(reverse("student:sheetboard", kwargs={"studentname": student.std_name}))

    def get_object(self, queryset=None):
        """
        Retrieves the Message object to read.
        """
        print('这里到底有没有调用啊？？？？？？？？？？？？')
        print(self.kwargs['sheet_slug'] + '     1231233132132132132123132')
        sheet = get_object_or_404(Sheet, sheet_slug=self.kwargs['sheet_slug'])
        # message.user=什么，我们先按下不表
        return sheet

    def get_context_data(self, **kwargs):
        sheet = get_object_or_404(Sheet, sheet_slug=self.kwargs['sheet_slug'])
        context = super(CreateAnswerView, self).get_context_data()
        student = get_object_or_404(Student, std_name=self.kwargs['studentname'])
        context['studentname'] = student.std_name
        print("检测这里又饿没有出错   " + context['studentname'])
        context['title'] = striptags(sheet.body)
        context['week_slug']=sheet.week_id
        return context


class SheetBoardView(ListView):
    template_name = 'student/sheet_board.html'
    context_object_name = 'sheets'

    def get_queryset(self):
        queryset = Sheet.objects.filter()
        queryset = queryset.order_by('-created_at')
        print("zheline")
        return queryset

    # def get_object(self, queryset=None):
    #     student = get_object_or_404(Student, student=self.kwargs['std_name'])
    #     # message.user=什么，我们先按下不表
    #     return student

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SheetBoardView, self).get_context_data()
        context['sheetboard'] = True
        print(self.kwargs['studentname'] + "    chuxianle shenme")
        student = get_object_or_404(Student, std_name=self.kwargs['studentname'])
        context['studentname'] = student.std_name
        print(context['studentname'] + "现在这个地方会不会显示呢")
        return context


class ReadSheet(DetailView):
    """
    View reading an existing Sheet object.
    """
    template_name = 'student/answers.html'
    context_object_name = 'sheet'
    print('这里开始运行了啦')

    def get_object(self, queryset=None):
        """
        Retrieves the Message object to read.
        """
        print(self.kwargs['sheet_slug'] + '     1231233132132132132123132')
        sheet = get_object_or_404(Sheet, sheet_slug=self.kwargs['sheet_slug'])
        # message.user=什么，我们先按下不表
        return sheet

    def get_context_data(self, **kwargs):
        """
        Provides extra context to the templates
        """
        context = super(ReadSheet, self).get_context_data(**kwargs)

        context['single_sheet'] = True
        return context


class CreateMessageView(CreateView):
    """
    View for creating new message object.
    """
    template_name = 'student/messages.html'
    form_class = MessageForm
    success_url = reverse_lazy("student:messages_list")

    def form_valid(self, form):
        """
        Instantiates a new Message object given a valid form.
        """
        student = get_object_or_404(Student, std_name=self.kwargs['studentname'])
        messages_form = MessageForm(self.request.POST)
        messages = messages_form.save(commit=False)
        slug = slugify(messages.title)
        messages.message_slug = slug
        messages.user=student.std_name
        messages.save()

        return HttpResponseRedirect(reverse("student:sheetboard", kwargs={"studentname": student.std_name}))

    def get_context_data(self, **kwargs):
        context = super(CreateMessageView, self).get_context_data(**kwargs)
        student = get_object_or_404(Student, std_name=self.kwargs['studentname'])
        context['studentname'] = student.std_name
        return context


class MessageList(ListView):
    """
    View for listing all message object.
    """
    template_name = 'student/messages_list.html'
    context_object_name = 'messages'

    '''我现在终于搞懂,get_queryset()是返回后台数据库中数据的一个方法'''

    def get_queryset(self):
        queryset = Message.objects.filter()
        for one_set in queryset:
            one_set.user = 'noname'
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MessageList, self).get_context_data(**kwargs)
        student = get_object_or_404(Student, std_name=self.kwargs['studentname'])
        context['studentname'] = student.std_name
        print(context['studentname'])
        return context


class ReadMessage(DetailView):
    """
    View reading an existing Message object.
    """
    template_name = 'student/messages_list.html'
    context_object_name = 'message'

    def get_object(self, queryset=None):
        """
        Retrieves the Message object to read.
        """
        print(self.kwargs['message_slug'])
        message = get_object_or_404(Message, message_slug=self.kwargs['message_slug'])
        # message.user=什么，我们先按下不表
        print(message.title + "  看一下这里有没有19191911919191919")
        return message

    def get_context_data(self, **kwargs):
        """
        Provides extra context to the templates
        """
        context = super(ReadMessage, self).get_context_data(**kwargs)
        context['single_message'] = True
        student = get_object_or_404(Student, std_name=self.kwargs['studentname'])
        context['studentname'] = student.std_name
        return context
