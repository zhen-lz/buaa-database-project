import json
import re

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app01.myForm import StuLoginForm, StuRegisterForm, TeacherRegisterForm, TeacherLoginForm
from app01.models import StudentInfo, TeacherInfo

import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='2872lizhen',
                     database='mydb')
cursor = db.cursor()


def toLogin(request):
    return render(request, 'login.html')


def toRegister(request):
    return render(request, 'toRegister.html')


def register(request):
    student_id = request.POST.get("student_id")
    passwd = request.POST.get("passwd")
    email = request.POST.get('email')
    realName = request.POST.get("realName")
    if student_id and passwd:
        cursor.execute(
            "insert into studentinfo(student_id,student_password, student_email, student_realName) values (\'{}\',\'{}\',\'{}\',\'{}\')".format(
                student_id, passwd, email, realName))
        return HttpResponse("注册成功,欢迎{}!".format(realName))
    else:
        return HttpResponse("学号和密码不得为空，请重新输入!")


def login(request):
    student_id = request.POST.get("student_id")
    passwd = request.POST.get("passwd")
    if student_id and passwd:
        cursor.execute(
            "select student_id from studentinfo where student_id=\'{}\' and student_password=\'{}\'".format(student_id,
                                                                                                            passwd))
        if cursor.fetchone() is None:
            return HttpResponse("账号密码错误，请输入正确的账号密码！")
        else:
            return HttpResponse("登陆成功!欢迎！")
    else:
        return HttpResponse("请输入正确的账号密码！")


# Create your views here.
def index(request):
    return HttpResponse("Welcome")


def user_list(request):
    return render(request, "user_list.html")


@csrf_exempt
def StudentRegister(request):
    if request.method == 'POST':
        print(request.POST)
        # print(json.decoder(request.POST))
        # print(json.loads(request.body))
        print(json.dumps(request.POST))
        # return json.dumps({'dd':'qw','as':'sas'}))

        stu_id = request.POST.get('student_id')
        password1 = request.POST.get('student_password1')
        password2 = request.POST.get('student_password2')
        email = request.POST.get('student_email')
        realName = request.POST.get('student_realName')

        findStuNo = "select * from studentinfo where student_id='{}'".format(stu_id)
        findEmail = "select * from studentinfo where student_email='{}'".format(email)
        cursor.execute(findStuNo)
        student = cursor.fetchall()
        if len(student) == 1:
            return JsonResponse({'error': 4006, 'msg': '当前学号已经存在，不能重复注册'})
        cursor.execute(findEmail)
        email = cursor.fetchall()
        if len(email) == 1:
            return JsonResponse({'error': 4007, 'msg': '当前邮箱已经存在，不能重复注册'})

        # 检测两次密码是否一致
        if password1 != password2:
            return JsonResponse({'error': 4004, 'msg': '两次输入的密码不一致'})
        # 检测密码不符合规范：8-18，英文字母+数字
        # if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
        #     return JsonResponse({'error': 4003, 'msg': '密码不符合规范'})

        # 成功
        # new_student = StudentInfo()
        # new_student.student_realName = realName
        # new_student.student_password = password1
        # new_student.student_email = email
        # new_student.student_id = stu_id
        # new_student.save()
        sql = "insert into studentinfo(student_id,student_password,student_email,student_realName) values ('{}','{}','{}','{}')".format(
            stu_id, password1, email, realName)
        cursor.execute(sql)
        db.commit()
        return JsonResponse({'error': 0, 'msg': '学生注册成功!'})

    return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def StudentLogin(request):
    # print(request.method)
    if request.method == 'POST':
        login_form = StuLoginForm(request.POST)
        print(request.POST)
        print(login_form)
        # print(login_form.cleaned_data.get('student_id'))
        # print(login_form.cleaned_data.get('student_password'))

        if login_form.is_valid():
            student_id = login_form.cleaned_data.get('student_id')
            student_password = login_form.cleaned_data.get('student_password')

            # try:
            #      user = StudentInfo.object.get(student_id=student_id)
            # except:
            #     return JsonResponse({'error': 4002, 'msg': '学号不存在'})
            sql = "select * from studentinfo where student_id='{}'".format(student_id)
            cnt = cursor.execute(sql)

            if cnt == 0:
                return JsonResponse({'code': 4002, 'msg': '学号不存在'})
            else:
                row = cursor.fetchone()
                print(row)
                if row[1] != student_password:
                    return JsonResponse({
                        'code': 4004,
                        'msg': "密码错误",
                    })
                else:
                    return JsonResponse({
                        'code': 0,
                        'msg': "登录成功",
                        'student_realName': row[3],
                        'email': row[2],
                    })

        return JsonResponse({'code': 8899, 'msg': '格式不对'})

    return JsonResponse({'code': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def TeacherRegister(request):
    if request.method == 'POST':
        register_form = TeacherRegisterForm(request.POST)
        if register_form.is_valid():
            teacher_id = register_form.cleaned_data.get('teacher_id')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            realName = register_form.cleaned_data.get('realName')

            # 检测两次密码是否一致
            if password1 != password2:
                return JsonResponse({'error': 4004, 'msg': '两次输入的密码不一致'})
            # 检测密码不符合规范：8-18，英文字母+数字
            if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
                return JsonResponse({'error': 4003, 'msg': '密码不符合规范'})

            # 成功
            # new_teacher = TeacherInfo()
            # new_teacher.teacher_id = teacher_id
            # new_teacher.teacher_password = password2
            # new_teacher.teacher_realName = realName
            # new_teacher.teacher_email = email
            # new_teacher.save()
            sql = 'insert into studentinfo(teacher_id,teacher_password,teacher_email,teacher_realName) values ("teacher_id","password1","email","realName")'
            cursor.execute(sql)
            db.commit()
            return JsonResponse({'error': 0, 'msg': '老师注册成功!'})
    return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def TeacherLogin(request):
    if request.method == 'POST':
        login_form = TeacherLoginForm(request.POST)

        if login_form.is_valid():
            teacher_id = login_form.cleaned_data.get('teacher_id')
            teacher_password = login_form.cleaned_data.get('teacher_password')
            # try:
            #     user = TeacherInfo.object.get(teacher_id=teacher_id)
            # except:
            #     return JsonResponse({'error': 4002, 'msg': '教工号不存在'})
            sql = "select * from teacherinfo where teacher_id='{}'".format(teacher_id)
            cnt = cursor.execute(sql)
            if cnt == 0:
                return JsonResponse({'error': 4002, 'msg': '教工号不存在'})
            else:
                row = cursor.fetchone()
                return JsonResponse({
                    'error': 0,
                    'msg': "登录成功",
                    'student_id': teacher_id,
                    'email': row[3],
                    'realName': row[4],
                })
    return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def update_pwd_student(request):
    if request.method == 'POST':
        register_email = request.POST.get("student_email")
        password = request.POST.get("password")
        try:
            user = StudentInfo.objects.get(student_email=register_email)
        except:
            return JsonResponse({'error': 4003, 'msg': '邮箱不存在'})
        if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password):
            return JsonResponse({'error': 4001, 'msg': '密码不符合规范'})
        user.userpassword = password
        user.save()
        del request.session["code"]  # 删除session
        msg = "密码已重置"
        return JsonResponse({'error': 0, 'msg': msg})

    return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def update_pwd_teacher(request):
    if request.method == 'POST':
        register_email = request.POST.get("teacher_email")
        password = request.POST.get("password")
        try:
            user = TeacherInfo.objects.get(teacher_email=register_email)
        except:
            return JsonResponse({'error': 4003, 'msg': '邮箱不存在'})
        if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password):
            return JsonResponse({'error': 4001, 'msg': '密码不符合规范'})
        user.userpassword = password
        user.save()
        del request.session["code"]  # 删除session
        msg = "密码已重置"
        return JsonResponse({'error': 0, 'msg': msg})

    return JsonResponse({'error': 2001, 'msg': '请求方式错误'})
