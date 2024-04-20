import json
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from userManage import models
from userManage.utils.form import TaskModelForm
from userManage.utils.pagination import Pagination


@csrf_exempt
def task_list(request):
    """任务管理"""
    # 获取数据库中的所有任务
    task_data = models.Task.objects.all().order_by("id")
    form = TaskModelForm()

    # 分页
    page_object = Pagination(request, task_data)

    context = {
        "task_data": page_object.page_queryset,
        "page_string": page_object.html(),
        "form": form
    }

    return render(request, "task_list.html", context)


@csrf_exempt  # 免除csrf_token认证
def task_add(request):
    """添加任务"""
    # print(request.POST)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {"status": False, "errors": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
