# Create your views here.
import json
import paddlehub as hub
from django.template.defaultfilters import striptags
from rest_framework.views import APIView
from pyecharts.charts import Line, Liquid, Grid
from pyecharts import options as opts
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from student.models import Message
from .models import Sheet, Teacher
from student.models import Student, Answer, Score
from .forms import SheetForm, TeacherLoginForm, TeacherRegisterForm


class BaseView(TemplateView):
    template_name = 'teacher/base_tch.html'


# Create your views here.
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


class StudentChartView(APIView):

    def get(self, request, *args, **kwargs):
        senta = hub.Module(name="senta_bilstm")
        student = get_object_or_404(Student, std_name=self.kwargs['studentname'])
        querysets = Answer.objects.filter(studentname=self.kwargs['studentname']).values_list('answer', flat=True)
        # print(querysets.count())
        querysetss = Answer.objects.filter(studentname=self.kwargs['studentname']).values_list('answer', flat=True)
        """????????????????????????"""
        week_num = 1
        queryset_weeks = []
        while week_num <= 10:
            queryset_weeks.append(
                Answer.objects.filter(studentname=self.kwargs['studentname'], week_id=week_num).values_list('answer',
                                                                                                            flat=True))
            week_num = week_num + 1
        print(queryset_weeks)
        """????????????????????????"""
        week_num = 1
        predict_answertext = []
        predict_answertexts = []

        for queryset_week in queryset_weeks:
            if week_num > 10:
                break
            else:
                for single_queryset in queryset_week:
                    predict_answertext.append(striptags(single_queryset))
                    # print(striptags(single_queryset))
                predict_answertexts.append(predict_answertext)
                predict_answertext = []
                week_num = week_num + 1
        print(predict_answertexts)
        """?????????score??????????????????"""
        positive_score = 0
        negative_score = 0
        result_num = 0
        result_num_help=0
        score_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        print('******')
        print(predict_answertexts)
        print('******')
        for predice_text in predict_answertexts:
            if len(predice_text) > 0:
                """senta????????????????????????"""
                results = senta.sentiment_classify(texts=predice_text, use_gpu=True, batch_size=1)
                print(results)
                if result_num > 11:
                    break
                else:
                    for result in results:
                        """?????????????????????????????????????????????"""
                        positive_score = positive_score + result['positive_probs']
                        negative_score = negative_score + result['negative_probs']
                    score_list[result_num]=round(positive_score / (positive_score + negative_score) * 10,2)

                    print('???'+result_num.__str__()+'???,positive_score???'+positive_score.__str__())
                    print('???'+result_num.__str__()+'???,negative_score???'+negative_score.__str__())
                    result_num = result_num + 1


        print(score_list)


        """?????????????????????????????????"""

        """????????????????????????????????????"""

        """
        line_chart ??????
        """

        line_chart = (
            Line()
                .add_xaxis(["?????????", "?????????", "?????????", "?????????", "?????????", "?????????", "?????????", "?????????", "?????????", "?????????"])
                .add_yaxis("?????? :  " + student.std_name, score_list)
                .set_global_opts(title_opts=opts.TitleOpts(title="?????????????????????", subtitle="", pos_left="3%"))
        )
        """
        liquid_chart ??????
        """
        depress_num = 0  # ??????????????????depress_value????????????
        depress_value = 0  # ???????????????????????????????????????
        lost_num = 0  # ?????????????????????????????????????????????lost_num??????1
        lost_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        a, m = 0, 0
        b = len(score_list) - 1
        n = len(score_list) - 1
        while a < b:
            if score_list[a + 1] < score_list[a]:
                lost_num = lost_num + 1
                lost_list[a] = 1

            a = a + 1
            print(a)
        # ?????????????????????????????????lost??????
        while m < n:
            if lost_list[m] == 1:
                depress_num = depress_num + 1
            else:
                depress_value = depress_num
                depress_num = 0
            m = m + 1
        if depress_value >= 4:
            depress_per = [0.99, ]
        else:
            depress_per = [lost_num / (len(score_list) - 1), ]
            print(lost_num)
            # print(score_list.count())
            print(depress_per)

        liquid_chart = (
            Liquid()
                .add(student.std_name, depress_per, center=["80%", "50%"], is_outline_show=False)
                .set_global_opts(title_opts=opts.TitleOpts(title="????????????", subtitle="????????????", pos_right="25%"))

        )

        """
        ?????????????????????????????????
        """
        grid = (
            Grid(init_opts=opts.InitOpts(width="1200px", height="800px"))
                .add(
                line_chart, grid_opts=opts.GridOpts(pos_right="40%"), is_control_axis_index=True
            )
                .add(liquid_chart, grid_opts=opts.GridOpts(pos_left="55%"), is_control_axis_index=True)
                .dump_options_with_quotes()
        )

        return JsonResponse(json.loads(grid))


class LoginIndexView(FormView):
    """
    Simple view for student login.
    """
    template_name = 'teacher/login.html'
    form_class = TeacherLoginForm
    success_url = reverse_lazy("teacher:students_list")

    def form_valid(self, form):

        teacher_form = TeacherLoginForm(self.request.POST)
        teacher = teacher_form.save(commit=False)
        teacher_v = get_object_or_404(Teacher, tch_id=teacher.tch_id)
        if teacher.tch_password == teacher_v.tch_password:
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect('teacher/login.html')


class CreateTeacherView(CreateView):
    """
    View for creating new sheet object.
    """
    template_name = 'teacher/register.html'
    form_class = TeacherRegisterForm
    success_url = reverse_lazy("teacher:login")

    def form_valid(self, form):
        teacher_form = TeacherRegisterForm(self.request.POST)
        teacher = teacher_form.save(commit=False)
        teacher.save()
        return HttpResponseRedirect(self.success_url)


class StudentList(ListView):
    """
    View for listing all student object.
    """
    template_name = 'teacher/students_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        print('?????????')
        queryset = Student.objects.filter()
        return queryset


class ReadStudent(DetailView, APIView):
    """
    View reading an existing Student object.
    """
    template_name = 'teacher/students_list.html'
    context_object_name = 'student'

    def get_object(self, queryset=None):
        """
        Retrieves the Message object to read.
        """
        student = get_object_or_404(Student, std_name=self.kwargs['student_slug'])

        # message.user=??????????????????????????????
        return student

    def get_score(self):
        student = get_object_or_404(Student, std_name=self.kwargs['student_slug'])
        queryset = Answer.objects.filter(studentname=student.std_name)

    def get_context_data(self, **kwargs):
        """
        Provides extra context to the templates
        """
        context = super(ReadStudent, self).get_context_data(**kwargs)
        context['single_student'] = True
        return context


class CreateSheetView(CreateView):
    """
    View for creating new sheet object.
    """
    template_name = 'teacher/sheets.html'
    form_class = SheetForm
    success_url = reverse_lazy("teacher:sheets_list")

    # def get_form_kwargs(self):
    #     form_kwargs = super().get_form_kwargs()
    #     try:
    #         if self.kwargs['course_id']:
    #             course = Course.objects.filter(course_slug=self.kwargs['course_id'])
    #             form_kwargs.update({'course': course})
    #     except KeyError:
    #         pass
    #     return form_kwargs

    def form_valid(self, form):
        """
        Instantiates a new Sheet object given a valid form.
        """
        sheets_form = SheetForm(self.request.POST)
        sheets = sheets_form.save(commit=False)
        slug = slugify(sheets.title)
        sheets.sheet_slug = slug
        sheets.save()
        return HttpResponseRedirect(self.success_url)


class MessageList(ListView):
    """
    View for listing all message object.
    """
    print('?????????111')
    template_name = 'teacher/messages_list.html'
    context_object_name = 'messages'

    '''?????????????????????,get_queryset()????????????????????????????????????????????????'''
    print('?????????222')

    def get_queryset(self):
        print('?????????')
        queryset = Message.objects.filter()
        # for one_set in queryset:
        #     one_set.user = 'who?' '''???????????????????????????????????????????????????'''
        return queryset


class ReadMessage(DetailView):
    """
    View reading an existing Message object.
    """
    template_name = 'teacher/messages_list.html'
    context_object_name = 'message'
    print('?????????333')

    def get_object(self, queryset=None):
        """
        Retrieves the Message object to read.
        """
        message = get_object_or_404(Message, message_slug=self.kwargs['message_slug'])
        # message.user=??????????????????????????????
        print('?????????')
        return message

    def get_context_data(self, **kwargs):
        """
        Provides extra context to the templates
        """
        context = super(ReadMessage, self).get_context_data(**kwargs)
        context['single_message'] = True
        return context


class SheetsList(ListView):
    """
    View for listing all message object.
    """
    template_name = 'teacher/sheets_list.html'
    context_object_name = 'sheets'

    '''?????????????????????,get_queryset()????????????????????????????????????????????????'''

    def get_queryset(self):
        queryset = Sheet.objects.filter()
        return queryset


class ReadSheet(DetailView):
    """
    View reading an existing Sheet object.
    """
    template_name = 'teacher/sheets_list.html'
    context_object_name = 'sheet'
    print('????????????????????????')

    def get_object(self, queryset=None):
        """
        Retrieves the Message object to read.
        """
        print(self.kwargs['sheet_slug'] + '     1231233132132132132123132')
        sheet = get_object_or_404(Sheet, sheet_slug=self.kwargs['sheet_slug'])
        # message.user=??????????????????????????????
        return sheet

    def get_context_data(self, **kwargs):
        """
        Provides extra context to the templates
        """
        context = super(ReadSheet, self).get_context_data(**kwargs)
        context['single_sheet'] = True
        return context
