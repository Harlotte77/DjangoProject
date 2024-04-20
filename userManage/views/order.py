import json
import random
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from userManage import models
from userManage.utils.pagination import Pagination
from userManage.utils.form import OrderModelForm


@csrf_exempt
def order_list(request):
    """订单列表"""
    order_data = models.Order.objects.all().order_by("order_id")
    form = OrderModelForm()
    # 分页
    page_object = Pagination(request, order_data)

    context = {
        "order_data": page_object.page_queryset,
        "page_string": page_object.html(),
        "form": form
    }
    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    """添加订单"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 从session获取当前登录的用户的ID作为订单表的admin_id字段
        form.instance.admin_id = request.session['info']['id']
        # 随机生成订单号
        form.instance.order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({'status': False, 'errors': form.errors})


def order_delete(request):
    """删除订单"""
    row_id = request.GET.get("row_id")
    exists = models.Order.objects.filter(id=row_id).exists()
    if not exists:
        return JsonResponse({"status": False, "errors": "删除失败，数据不存在"})
    models.Order.objects.filter(id=row_id).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """订单详情"""
    row_id = request.GET.get("row_id")
    row_dict = models.Order.objects.filter(id=row_id).values("order_name", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, "errors": "数据不存在"})

    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """编辑订单"""
    row_id = request.GET.get("row_id")
    row_object = models.Order.objects.filter(id=row_id).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "数据不存在, 可能已被删除，请刷新重试"})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "errors": form.errors})
