from django.shortcuts import render, redirect
from userManage import models
from userManage.utils.form import PretyModelForm, PrettyEditModelForm
from userManage.utils.pagination import Pagination


def prettynum_list(request):
    """显示所有的靓号"""
    # 按照级别大小排序
    # .order_by("-level")表示倒序排序(从大到小)
    # .order_by("level")表示正序排序(从小到大)
    dict_data = {}
    search_data = request.GET.get("query", "")
    if search_data:
        dict_data['mobile__contains'] = search_data
    prettynum_data = models.PrettyNum.objects.filter(**dict_data).order_by("-level")

    # 分页
    page_object = Pagination(request, prettynum_data)
    context = {
        "prettynum_data": page_object.page_queryset,
        "page_string": page_object.html(),
        "search_data": search_data
    }

    return render(request, 'prettynum_list.html', context)


def prettynum_add(request):
    """新建靓号"""
    if request.method == 'GET':
        form = PretyModelForm()
        return render(request, 'prettynum_add.html', {'form': form})

    form = PretyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    return render(request, 'prettynum_add.html', {'form': form})


def prettynum_edit(request, pretty_id):
    """编辑靓号"""
    pretty_data = models.PrettyNum.objects.filter(id=pretty_id).first()
    if request.method == 'GET':
        form = PrettyEditModelForm(instance=pretty_data)
        return render(request, 'prettynum_edit.html', {'form': form})
    form = PrettyEditModelForm(data=request.POST, instance=pretty_data)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    return render(request, 'prettynum_edit.html', {'form': form})


def prettynum_delete(request, pretty_id):
    """靓号删除"""
    models.PrettyNum.objects.filter(id=pretty_id).delete()
    return redirect('/prettynum/list/')
