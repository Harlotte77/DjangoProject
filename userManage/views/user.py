from userManage import models
from django.shortcuts import render, redirect
from userManage.utils.form import UserModelForm
from userManage.utils.pagination import Pagination


def user_list(request):
    """用户管理"""
    user_data = models.UserInfo.objects.all()

    # 分页
    page_object = Pagination(request, user_data)
    context = {
        "user_data": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """添加员工"""
    if request.method == 'GET':
        context = {
            'gender_choice': models.UserInfo.gender_choice,
            'depart_data': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)
    # 获取用户提交的数据
    name = request.POST.get('name')
    password = request.POST.get('password')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    salary = request.POST.get('salary')
    create_time = request.POST.get('create_time')
    depart = request.POST.get('depart')
    models.UserInfo.objects.create(name=name, password=password, age=age, gender=gender, salary=salary,
                                   create_time=create_time, user_depart_id=depart)
    return redirect('/user/list/')


def user_add_ModelForm(request):
    """使用ModelForm完成添加用户的功能"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add_ModelForm.html', {'form': form})

    # 获取用户输入，并进行数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，则保存到数据库
        # print(form.cleaned_data)
        # {'name': '123', 'password': '123333', 'age': 131233, 'gender': 1, 'salary': Decimal('10000'),
        # 'create_time': datetime.datetime(2021, 10, 12, 0, 0, tzinfo=backports.zoneinfo.ZoneInfo(key='UTC')),
        # 'user_depart': <Department: 策划部>}

        # 自动保存到数据库
        # 默认保存的是用户输入的所有数据，但是如果想要保存除用户输入以外的数据，则需要额外自定义
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_add_ModelForm.html', {'form': form})


def user_edit(request, user_id):
    """修改员工信息"""
    user_row_data = models.UserInfo.objects.filter(id=user_id).first()
    if request.method == 'GET':
        form = UserModelForm(instance=user_row_data)
        return render(request, 'user_edit.html', {'form': form})
    form = UserModelForm(data=request.POST, instance=user_row_data)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, user_id):
    """删除员工信息"""
    models.UserInfo.objects.filter(id=user_id).delete()
    return redirect('/user/list/')
