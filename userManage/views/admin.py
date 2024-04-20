from django.shortcuts import render, redirect
from userManage import models
from userManage.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from userManage.utils.pagination import Pagination

def admin_list(request):
    """管理员"""
    dict_data = {}
    search_data = request.GET.get("query", "")
    if search_data:
        dict_data["username__contains"] = search_data
    # 根据搜索条件去数据库获取信息
    admin_data = models.Admin.objects.filter(**dict_data)

    # 分页
    page_object = Pagination(request, admin_data)
    context = {
        'admin_data': page_object.page_queryset,
        "page_string": page_object.html(),
        'search_data': search_data,
    }
    return render(request, "admin_list.html", context)


def admin_add_ModelForm(request):
    """新建管理员"""

    title = '新建管理员'
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {'title': title, 'form': form})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'change.html', {'title': title, 'form': form})


def admin_edit(request, admin_id):
    """编辑管理员信息"""
    title = "编辑管理员"
    admin_data = models.Admin.objects.filter(id=admin_id).first()
    # if admin_data:
    #     return redirect('/admin/list')

    if request.method == 'GET':
        form = AdminEditModelForm(instance=admin_data)
        return render(request, 'change.html', {'title': title, 'form': form})
    form = AdminEditModelForm(data=request.POST, instance=admin_data)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'change.html', {'title': title, 'form': form})

def admin_delete(request, admin_id):
    """删除管理员"""
    models.Admin.objects.filter(id=admin_id).delete()
    return redirect('/admin/list/')

def admin_reset(request, admin_id):
    """管理员密码重置"""
    admin_data = models.Admin.objects.filter(id=6).first()
    if not admin_data:
        return redirect('/admin/list')
    title = "重置密码 - {}".format(admin_data.username)
    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'title': title, 'form': form})
    form = AdminResetModelForm(data=request.POST, instance=admin_data)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'change.html', {'title': title, 'form': form})

